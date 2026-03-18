"""
YojanaGPT - Unified LLM Client
Supports Groq (free), Ollama (local), and Gemini (free tier).
Automatic fallback between providers.
"""

import json
import time
import logging
import requests
from typing import Optional, Generator
from config.settings import llm_config, LLMProvider

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified LLM client with multi-provider support and automatic fallback."""
    
    def __init__(self):
        self.config = llm_config
        self._provider_order = self._build_provider_order()
        self._rate_limit_tracker = {}
        
    def _build_provider_order(self) -> list:
        """Build provider fallback order based on available credentials."""
        order = []
        if self.config.groq_api_key:
            order.append(LLMProvider.GROQ)
        if self.config.gemini_api_key:
            order.append(LLMProvider.GEMINI)
        order.append(LLMProvider.OLLAMA)  # Always available as last resort
        return order
    
    def _check_rate_limit(self, provider: str) -> bool:
        """Check if we're rate-limited for a provider."""
        if provider in self._rate_limit_tracker:
            cooldown_until = self._rate_limit_tracker[provider]
            if time.time() < cooldown_until:
                return False
        return True
    
    def _set_rate_limit(self, provider: str, seconds: int = 60):
        """Mark a provider as rate-limited."""
        self._rate_limit_tracker[provider] = time.time() + seconds
    
    # ─── Groq ─────────────────────────────────────────────────────────
    def _call_groq(self, messages: list, temperature: float = None, 
                   max_tokens: int = None, json_mode: bool = False) -> str:
        """Call Groq API (Llama 3.3 70B)."""
        from groq import Groq
        
        client = Groq(api_key=self.config.groq_api_key)
        
        kwargs = {
            "model": self.config.groq_model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        try:
            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                logger.warning(f"Groq rate limited, cooling down: {error_msg}")
                self._set_rate_limit(LLMProvider.GROQ, 60)
                # Try with fallback model
                try:
                    kwargs["model"] = self.config.groq_fallback_model
                    response = client.chat.completions.create(**kwargs)
                    return response.choices[0].message.content
                except Exception:
                    raise
            raise
    
    # ─── Ollama ───────────────────────────────────────────────────────
    def _call_ollama(self, messages: list, temperature: float = None,
                     max_tokens: int = None, json_mode: bool = False) -> str:
        """Call local Ollama instance."""
        url = f"{self.config.ollama_base_url}/api/chat"
        
        payload = {
            "model": self.config.ollama_model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature or self.config.temperature,
                "num_predict": max_tokens or self.config.max_tokens,
            }
        }
        
        if json_mode:
            payload["format"] = "json"
        
        try:
            response = requests.post(url, json=payload, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()["message"]["content"]
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Ollama is not running. Start it with: ollama serve\n"
                "Then pull a model: ollama pull llama3.2"
            )
        except Exception as e:
            raise RuntimeError(f"Ollama error: {e}")
    
    # ─── Gemini ───────────────────────────────────────────────────────
    def _call_gemini(self, messages: list, temperature: float = None,
                     max_tokens: int = None, json_mode: bool = False) -> str:
        """Call Google Gemini API (free tier)."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.gemini_model}:generateContent"
        
        # Convert messages to Gemini format
        contents = []
        system_text = ""
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            elif msg["role"] == "user":
                contents.append({"role": "user", "parts": [{"text": msg["content"]}]})
            elif msg["role"] == "assistant":
                contents.append({"role": "model", "parts": [{"text": msg["content"]}]})
        
        # Prepend system message to first user message if exists
        if system_text and contents:
            first_content = contents[0]["parts"][0]["text"]
            contents[0]["parts"][0]["text"] = f"[System Instruction]: {system_text}\n\n{first_content}"
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature or self.config.temperature,
                "maxOutputTokens": max_tokens or self.config.max_tokens,
            }
        }
        
        if json_mode:
            payload["generationConfig"]["responseMimeType"] = "application/json"
        
        try:
            response = requests.post(
                url,
                params={"key": self.config.gemini_api_key},
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            if "429" in str(e):
                self._set_rate_limit(LLMProvider.GEMINI, 60)
            raise
    
    # ─── Main Call Method ─────────────────────────────────────────────
    def chat(self, messages: list, temperature: float = None,
             max_tokens: int = None, json_mode: bool = False,
             preferred_provider: LLMProvider = None) -> str:
        """
        Send a chat request with automatic fallback between providers.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max tokens
            json_mode: If True, request JSON output format
            preferred_provider: Force a specific provider
            
        Returns:
            LLM response text
        """
        providers = [preferred_provider] if preferred_provider else self._provider_order
        last_error = None
        
        for provider in providers:
            if not self._check_rate_limit(provider):
                logger.info(f"Skipping {provider} (rate limited)")
                continue
            
            try:
                logger.info(f"Calling {provider}...")
                
                if provider == LLMProvider.GROQ:
                    return self._call_groq(messages, temperature, max_tokens, json_mode)
                elif provider == LLMProvider.OLLAMA:
                    return self._call_ollama(messages, temperature, max_tokens, json_mode)
                elif provider == LLMProvider.GEMINI:
                    return self._call_gemini(messages, temperature, max_tokens, json_mode)
                    
            except Exception as e:
                last_error = e
                logger.warning(f"{provider} failed: {e}")
                continue
        
        raise RuntimeError(
            f"All LLM providers failed. Last error: {last_error}\n\n"
            "Please ensure at least one of:\n"
            "1. GROQ_API_KEY is set in .env (free at console.groq.com)\n"
            "2. GEMINI_API_KEY is set in .env (free at aistudio.google.com)\n"
            "3. Ollama is running locally (ollama serve)"
        )
    
    def get_active_provider(self) -> str:
        """Return the name of the currently active provider."""
        for provider in self._provider_order:
            if self._check_rate_limit(provider):
                return provider.value
        return "none"

    def has_remote_llm(self) -> bool:
        """Return True when a cloud LLM provider is configured."""
        return bool(self.config.groq_api_key or self.config.gemini_api_key)


# Singleton
llm_client = LLMClient()
