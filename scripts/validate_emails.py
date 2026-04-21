#!/usr/bin/env python3
"""Validate emails via Clearout API (instant single-email verification).

Self-healing: validates response shape on every call. If the API changes
its response format, reports the discrepancy clearly instead of silently
returning bad data.

Usage:
  # Single email
  python3 scripts/validate_emails.py --email someone@example.com

  # Batch from stdin (one email per line)
  cat emails.txt | python3 scripts/validate_emails.py

  # Batch from file
  python3 scripts/validate_emails.py --file emails.txt

Output: JSON to stdout
  {
    "results": [
      {
        "email": "someone@example.com",
        "verdict": "valid",       # valid | invalid | risky | unknown
        "safe_to_send": "yes",    # yes | no | risky | unknown
        "reason": "Success",
        "disposable": false,
        "role": false,
        "free": false,
        "provider": "clearout"
      }
    ],
    "summary": { "total": 1, "valid": 1, "invalid": 0, "risky": 0, "unknown": 0 },
    "errors": []
  }

Environment:
  CLEAROUT_API_KEY — Required. Bearer token from Clearout dashboard.

Rate limits:
  Respects x-ratelimit-remaining header. Pauses when near limit.
  Default: processes up to 25/min on low-tier plans.
"""

import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests not installed. Run: pip3 install requests"}))
    sys.exit(1)


# --- Config ---

API_BASE = "https://api.clearout.io/v2"
VERIFY_ENDPOINT = f"{API_BASE}/email_verify/instant"
TIMEOUT_MS = 130000  # Clearout default

# Expected fields in a valid response — used for self-healing checks
EXPECTED_RESPONSE_KEYS = {"status", "data"}
EXPECTED_DATA_KEYS = {"email_address", "status", "safe_to_send"}

# Map Clearout statuses to our standardized verdicts
STATUS_MAP = {
    "valid": "valid",
    "invalid": "invalid",
    "catch_all": "risky",
    "unknown": "unknown",
}

SAFE_TO_SEND_MAP = {
    "yes": "yes",
    "no": "no",
    "risky": "risky",
    "unknown": "unknown",
}


# --- Self-healing response validation ---

def validate_response_shape(resp_json):
    """Check that the API response matches expected structure.

    Returns (is_valid, warning_message). If the shape changed,
    we still try to extract what we can but report the discrepancy.
    """
    warnings = []

    if not isinstance(resp_json, dict):
        return False, "Response is not a JSON object"

    missing_top = EXPECTED_RESPONSE_KEYS - set(resp_json.keys())
    if missing_top:
        warnings.append(f"Missing top-level keys: {missing_top}")

    data = resp_json.get("data", {})
    if isinstance(data, dict):
        missing_data = EXPECTED_DATA_KEYS - set(data.keys())
        if missing_data:
            warnings.append(f"Missing data keys: {missing_data}")
    else:
        warnings.append(f"'data' field is {type(data).__name__}, expected dict")

    if warnings:
        return False, "; ".join(warnings)
    return True, ""


def extract_result(resp_json, email):
    """Extract standardized result from Clearout response.

    Resilient: uses .get() with fallbacks so partial responses
    still produce usable output.
    """
    data = resp_json.get("data", {})

    raw_status = data.get("status", "unknown")
    raw_safe = data.get("safe_to_send", "unknown")

    # Map to our standard verdicts, falling back gracefully
    verdict = STATUS_MAP.get(raw_status, "unknown")
    safe_to_send = SAFE_TO_SEND_MAP.get(raw_safe, "unknown")

    sub_status = data.get("sub_status", {})
    reason = sub_status.get("desc", raw_status) if isinstance(sub_status, dict) else raw_status

    return {
        "email": email,
        "verdict": verdict,
        "safe_to_send": safe_to_send,
        "reason": reason,
        "disposable": data.get("disposable", "no") == "yes",
        "role": data.get("role", "no") == "yes",
        "free": data.get("free", "no") == "yes",
        "provider": "clearout",
    }


# --- API interaction ---

def get_api_key():
    """Load API key from environment or .env.local file."""
    key = os.environ.get("CLEAROUT_API_KEY")
    if key:
        return key

    # Try .env.local in project root
    env_paths = [
        Path(__file__).parent.parent / ".env.local",
        Path.cwd() / ".env.local",
    ]
    for env_path in env_paths:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line.startswith("CLEAROUT_API_KEY=") and not line.startswith("#"):
                    return line.split("=", 1)[1].strip().strip("'\"")

    return None


def verify_single(email, api_key, session):
    """Verify a single email. Returns (result_dict, error_string_or_None)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"email": email, "timeout": TIMEOUT_MS}

    try:
        resp = session.post(VERIFY_ENDPOINT, json=payload, headers=headers, timeout=140)
    except requests.Timeout:
        return None, f"HTTP timeout verifying {email}"
    except requests.RequestException as e:
        return None, f"Request failed for {email}: {e}"

    # Rate limit handling
    remaining = resp.headers.get("x-ratelimit-remaining")
    if remaining is not None and int(remaining) <= 1:
        reset_secs = int(resp.headers.get("x-ratelimit-reset", 60))
        time.sleep(min(reset_secs, 65))

    if resp.status_code == 429:
        reset_secs = int(resp.headers.get("x-ratelimit-reset", 60))
        return None, f"Rate limited on {email}. Retry after {reset_secs}s."

    if resp.status_code == 401:
        return None, "Invalid API key (401 Unauthorized)"

    if resp.status_code == 402:
        return None, "Insufficient credits (402 Payment Required)"

    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code} for {email}: {resp.text[:200]}"

    try:
        resp_json = resp.json()
    except ValueError:
        return None, f"Non-JSON response for {email}: {resp.text[:200]}"

    # Self-healing check
    shape_ok, shape_warning = validate_response_shape(resp_json)
    result = extract_result(resp_json, email)

    if not shape_ok:
        result["_schema_warning"] = shape_warning

    return result, None


# --- Main ---

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate emails via Clearout API")
    parser.add_argument("--email", help="Single email to validate")
    parser.add_argument("--file", help="File with one email per line")
    parser.add_argument("--delay", type=float, default=1.5,
                        help="Seconds between requests (default: 1.5)")
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print(json.dumps({"error": "CLEAROUT_API_KEY not found in environment or .env.local"}))
        sys.exit(1)

    # Collect emails
    emails = []
    if args.email:
        emails = [args.email.strip()]
    elif args.file:
        emails = [line.strip() for line in Path(args.file).read_text().splitlines() if line.strip() and "@" in line]
    elif not sys.stdin.isatty():
        emails = [line.strip() for line in sys.stdin if line.strip() and "@" in line]
    else:
        print(json.dumps({"error": "No emails provided. Use --email, --file, or pipe to stdin."}))
        sys.exit(1)

    results = []
    errors = []
    session = requests.Session()

    for i, email in enumerate(emails):
        result, error = verify_single(email, api_key, session)
        if error:
            errors.append(error)
            # Still produce a result entry for the email
            results.append({
                "email": email,
                "verdict": "unknown",
                "safe_to_send": "unknown",
                "reason": error,
                "disposable": False,
                "role": False,
                "free": False,
                "provider": "clearout",
            })
        else:
            results.append(result)

        # Rate-limit courtesy delay between requests
        if i < len(emails) - 1:
            time.sleep(args.delay)

    # Summary
    summary = {
        "total": len(results),
        "valid": sum(1 for r in results if r["verdict"] == "valid"),
        "invalid": sum(1 for r in results if r["verdict"] == "invalid"),
        "risky": sum(1 for r in results if r["verdict"] == "risky"),
        "unknown": sum(1 for r in results if r["verdict"] == "unknown"),
    }

    output = {"results": results, "summary": summary, "errors": errors}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
