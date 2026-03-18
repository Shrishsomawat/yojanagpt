"""Utilities for reviewing scheme freshness in the local database."""

from __future__ import annotations

from datetime import date, datetime

from data.schemes_database import get_all_schemes


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def build_review_report() -> dict:
    """Build a freshness report for all schemes."""
    today = date.today()
    schemes = get_all_schemes()

    verified = []
    needs_review = []
    overdue = []
    archived = []

    for scheme in schemes:
        record = {
            "id": scheme["id"],
            "name": scheme["name"],
            "status": scheme.get("verification_status", "needs_review"),
            "last_verified_on": scheme.get("last_verified_on"),
            "review_due_on": scheme.get("review_due_on"),
            "source": scheme.get("source_name"),
        }

        if record["status"] == "verified":
            verified.append(record)

            review_due = _parse_date(record["review_due_on"])
            if review_due and review_due < today:
                overdue.append(record)
        elif record["status"] == "archived":
            archived.append(record)
        else:
            needs_review.append(record)

    verified.sort(key=lambda item: (item["review_due_on"] or "9999-99-99", item["id"]))
    needs_review.sort(key=lambda item: item["id"])
    overdue.sort(key=lambda item: (item["review_due_on"] or "9999-99-99", item["id"]))
    archived.sort(key=lambda item: item["id"])

    return {
        "today": today.isoformat(),
        "total": len(schemes),
        "verified": verified,
        "needs_review": needs_review,
        "overdue": overdue,
        "archived": archived,
    }


def print_review_report() -> None:
    """Print a human-friendly freshness report."""
    report = build_review_report()

    print("\n" + "=" * 72)
    print("YojanaGPT Scheme Freshness Review")
    print("=" * 72)
    print(f"Date: {report['today']}")
    print(f"Total schemes: {report['total']}")
    print(f"Verified: {len(report['verified'])}")
    print(f"Needs review: {len(report['needs_review'])}")
    print(f"Archived / excluded: {len(report['archived'])}")
    print(f"Overdue verified schemes: {len(report['overdue'])}")

    if report["overdue"]:
        print("\nOverdue Verified Schemes")
        print("-" * 72)
        for item in report["overdue"]:
            print(f"{item['id']:<20} review due {item['review_due_on']}  source: {item['source']}")

    if report["archived"]:
        print("\nArchived Or Excluded Schemes")
        print("-" * 72)
        for item in report["archived"][:15]:
            print(f"{item['id']:<20} status: {item['status']}  source: {item['source']}")

    print("\nNext Schemes To Review")
    print("-" * 72)
    preview = report["needs_review"][:15]
    if not preview:
        print("No unverified schemes left.")
    else:
        for item in preview:
            print(f"{item['id']:<20} status: {item['status']}")

    print("=" * 72 + "\n")


if __name__ == "__main__":
    print_review_report()
