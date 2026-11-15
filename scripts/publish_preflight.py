#!/usr/bin/env python3
"""Check LinkedIn authentication before spending on generation or posting elsewhere.

No publishing endpoints are called. Success checks identity only, not every
upload/post permission. Never print credentials or provider error bodies.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import platforms


def check_linkedin():
    if int(os.environ.get("LINKEDIN_POSTS_PER_DAY", "1")) <= 0:
        return
    token = platforms._linkedin_token()
    response = platforms.requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    response.raise_for_status()
    if not response.json().get("sub"):
        raise RuntimeError("LinkedIn identity response has no subject")


def main():
    try:
        check_linkedin()
    except Exception:
        raise SystemExit("LinkedIn authentication preflight failed; renew or verify repository credentials before publishing.")
    print("LinkedIn identity preflight passed; publishing permissions are not fully tested.")


if __name__ == "__main__":
    main()
