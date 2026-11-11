from __future__ import annotations

import hashlib
import logging
import re
import secrets
from typing import Any

import requests
from flask import Flask, jsonify, render_template, request
from zxcvbn import zxcvbn

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 256 * 1024  # Limit uploads to 256 KB.

# Avoid Flask's request log output. The app never logs request bodies or passwords.
logging.getLogger("werkzeug").setLevel(logging.ERROR)

HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/"
HIBP_TIMEOUT_SECONDS = 5

# Small, local starter blocklist. Extend this file/list with organization-approved
# common-password entries if needed. Never upload passwords to build this list.
COMMON_PASSWORDS = {
    "123456", "123456789", "12345678", "12345", "1234567",
    "password", "password1", "password123", "qwerty", "qwerty123",
    "abc123", "111111", "123123", "iloveyou", "admin",
    "letmein", "welcome", "monkey", "dragon", "football",
    "sunshine", "princess", "login", "passw0rd", "P@ssw0rd",
}

SEQUENCE_PATTERNS = (
    "1234", "2345", "3456", "4567", "5678", "6789",
    "9876", "8765", "7654", "6543", "5432", "4321",
    "abcd", "bcde", "cdef", "qwerty", "asdf", "zxcv",
)


def character_classes(password: str) -> dict[str, bool]:
    return {
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digits": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[^A-Za-z0-9]", password)),
    }


def local_pattern_checks(password: str) -> dict[str, Any]:
    lowered = password.lower()
    repeated = bool(re.search(r"(.)\1{2,}", password))
    sequence_matches = sorted({p for p in SEQUENCE_PATTERNS if p in lowered})
    common = lowered in {item.lower() for item in COMMON_PASSWORDS}
    return {
        "repeated_characters": repeated,
        "predictable_sequences": sequence_matches,
        "common_password": common,
    }


def hibp_check(password: str) -> dict[str, Any]:
    """HIBP k-anonymity range query: only SHA-1's first five hex chars leave the host."""
    sha1_hex = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_hex[:5], sha1_hex[5:]
    try:
        response = requests.get(
            HIBP_RANGE_URL + prefix,
            headers={
                "User-Agent": "LocalPasswordSecurityAuditor/1.0",
                "Add-Padding": "true",
            },
            timeout=HIBP_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        for line in response.text.splitlines():
            parts = line.strip().split(":")
            if len(parts) == 2 and secrets.compare_digest(parts[0].upper(), suffix):
                return {
                    "status": "found",
                    "count": int(parts[1]),
                    "message": "This password appears in the Pwned Passwords dataset.",
                }
        return {
            "status": "not_found",
            "count": 0,
            "message": "No match was returned by Pwned Passwords. This does not prove the password is safe.",
        }
    except requests.RequestException:
        return {
            "status": "unavailable",
            "count": None,
            "message": "The breach check could not be completed. Check connectivity and try again.",
        }


def crack_time_label(zxcvbn_result: dict[str, Any]) -> str:
    # zxcvbn returns attack-specific estimates. Use an offline slow-hash scenario
    # only as an illustrative category; it is not a promise about real cracking time.
    seconds = zxcvbn_result.get("crack_times_seconds", {}).get(
        "offline_slow_hashing_1e4_per_second"
    )
    if seconds is None:
        return "Unavailable"
    if seconds < 1:
        return "Less than a second"
    if seconds < 60:
        return "Seconds"
    if seconds < 3600:
        return "Minutes"
    if seconds < 86400:
        return "Hours"
    if seconds < 31557600:
        return "Days to months"
    if seconds < 31557600 * 100:
        return "Years to decades"
    return "Centuries or longer"


def analyze_password(password: str, check_breach: bool = True) -> dict[str, Any]:
    if not isinstance(password, str) or not password:
        raise ValueError("Password cannot be empty.")
    if len(password) > 256:
        raise ValueError("Password is too long for this demo (maximum 256 characters).")

    classes = character_classes(password)
    patterns = local_pattern_checks(password)
    strength = zxcvbn(password)
    score = int(strength.get("score", 0))

    # zxcvbn's score is the primary estimate. Do not infer strength from entropy
    # or character classes alone. Common/pattern matches are important warnings.
    labels = ["Weak", "Weak", "Moderate", "Strong", "Strong"]
    rating = labels[score]
    if patterns["common_password"] or patterns["repeated_characters"] or patterns["predictable_sequences"]:
        if rating == "Strong":
            rating = "Moderate"
        elif rating == "Moderate":
            rating = "Weak"

    breach = hibp_check(password) if check_breach else {
        "status": "not_checked", "count": None, "message": "Breach check skipped."
    }

    suggestions = []
    if len(password) < 14:
        suggestions.append("Use a longer password or unique passphrase (aim for 14–16+ characters).")
    if patterns["common_password"]:
        suggestions.append("Replace this common password with a unique password.")
    if patterns["repeated_characters"]:
        suggestions.append("Avoid repeated-character patterns.")
    if patterns["predictable_sequences"]:
        suggestions.append("Avoid keyboard or sequential patterns.")
    if score <= 2:
        suggestions.append("Use a randomly generated password or a long, unique passphrase.")
    if breach["status"] == "found":
        suggestions.append("Change this password anywhere it is used; do not reuse exposed passwords.")
    if breach["status"] == "unavailable":
        suggestions.append("Retry the breach check when network access is available.")
    if not suggestions:
        suggestions.append("Keep it unique to one account and store it in a reputable password manager.")

    return {
        "strength": rating,
        "length": len(password),
        "classes": classes,
        "class_count": sum(classes.values()),
        "zxcvbn_score": score,
        "zxcvbn_label": strength.get("feedback", {}).get("warning") or "No major warning from zxcvbn.",
        "guesses": strength.get("guesses"),
        "crack_time_estimate": crack_time_label(strength),
        "common_password": patterns["common_password"],
        "repeated_characters": patterns["repeated_characters"],
        "predictable_sequences": patterns["predictable_sequences"],
        "breach": breach,
        "recommendations": suggestions,
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    password = payload.get("password")
    check_breach = bool(payload.get("check_breach", True))
    try:
        result = analyze_password(password, check_breach=check_breach)
        return jsonify({"ok": True, "result": result})
    except (ValueError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.post("/api/analyze-list")
def analyze_list():
    """Process newline-delimited passwords in memory; never write the upload to disk."""
    uploaded = request.files.get("file")
    if not uploaded:
        return jsonify({"ok": False, "error": "Choose a text file first."}), 400
    try:
        raw = uploaded.stream.read(256 * 1024 + 1)
        if len(raw) > 256 * 1024:
            return jsonify({"ok": False, "error": "File exceeds the 256 KB limit."}), 413
        lines = raw.decode("utf-8-sig").splitlines()
        passwords = [line.strip() for line in lines if line.strip()]
        if not passwords:
            return jsonify({"ok": False, "error": "No non-empty password lines were found."}), 400
        if len(passwords) > 50:
            return jsonify({"ok": False, "error": "Maximum 50 passwords per import."}), 400

        results = []
        for index, password in enumerate(passwords, start=1):
            try:
                results.append({
                    "index": index,
                    "result": analyze_password(password, check_breach=True),
                })
            except ValueError as exc:
                results.append({"index": index, "error": str(exc)})
        return jsonify({"ok": True, "results": results})
    finally:
        # Drop references as soon as the request is complete.
        uploaded = None


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"ok": False, "error": "Upload exceeds the 256 KB limit."}), 413


if __name__ == "__main__":
    # Localhost only: this is intentionally not exposed to the LAN.
    app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False)
