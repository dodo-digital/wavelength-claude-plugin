#!/usr/bin/env python3
"""Format enriched contacts into master CSV + Reply.io upload CSV.

Usage: python3 format_output.py <industry> <output_dir>
Input: JSON from stdin (enriched contacts array)
Output: JSON to stdout with file paths created.

Expected stdin format:
{
  "contacts": [
    {
      "email": "john@acme.com",
      "first_name": "John",
      "last_name": "Smith",
      "company_name": "Acme Fire",
      "title": "Owner",
      "industry": "fire safety",
      "business_model": "fire inspection and code compliance",
      "year_founded": "1998",
      "city": "Dallas",
      "state": "TX",
      "linkedin_profile": "https://linkedin.com/in/jsmith",
      "clearout_rating": "safe",
      "zerobounce_rating": "valid",
      ...
    }
  ]
}
"""

import csv
import json
import sys
from datetime import date
from pathlib import Path

# Master CSV columns — all fields
MASTER_COLS = [
    "email", "first_name", "last_name", "company_name", "title",
    "industry", "business_model", "year_founded", "city", "state",
    "linkedin_profile", "clearout_rating", "zerobounce_rating",
    "revenue", "employees", "website", "age", "description",
]

# Reply.io upload columns — green + yellow only (no red validation cols)
REPLY_COLS = [
    "email", "first_name", "last_name", "company_name", "title",
    "industry", "business_model", "year_founded", "city", "state",
    "linkedin_profile",
]

# Columns to exclude from Reply.io upload based on validation status
DO_NOT_SEND_STATUSES = ["invalid", "disposable", "hard"]


def is_safe_to_send(contact: dict) -> bool:
    """Check if a contact's email is safe enough for Reply.io."""
    clearout = (contact.get("clearout_rating") or "").lower()
    zerobounce = (contact.get("zerobounce_rating") or "").lower()

    for status in DO_NOT_SEND_STATUSES:
        if status in clearout or status in zerobounce:
            return False
    return True


def write_csv(contacts: list, columns: list, path: str):
    """Write contacts to CSV with specified columns."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)


def main():
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: format_output.py <industry> <output_dir>"}))
        sys.exit(1)

    industry = sys.argv[1].lower().replace(" ", "-")
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(sys.stdin.read())
    contacts = data.get("contacts", [])

    today = date.today().isoformat()
    master_path = output_dir / f"{industry}-{today}-master.csv"
    reply_path = output_dir / f"{industry}-{today}-reply-io.csv"

    # Master CSV — all contacts, all columns
    write_csv(contacts, MASTER_COLS, str(master_path))

    # Reply.io CSV — only sendable contacts, green+yellow columns only
    sendable = [c for c in contacts if is_safe_to_send(c)]
    not_sendable = [c for c in contacts if not is_safe_to_send(c)]

    write_csv(sendable, REPLY_COLS, str(reply_path))

    result = {
        "master_csv": str(master_path),
        "reply_io_csv": str(reply_path),
        "total_contacts": len(contacts),
        "sendable": len(sendable),
        "blocked_by_validation": len(not_sendable),
        "blocked_emails": [c.get("email", "") for c in not_sendable],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
