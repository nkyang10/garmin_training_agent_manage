# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Active |

## What This Project Protects

This project handles **Garmin Connect credentials** (email + password) and communicates with Garmin's official API. Your credentials grant access to personal health data including:

- Heart rate, HRV, and stress history
- Sleep tracking data
- GPS location history from activities
- Body composition (weight, BMI, body fat)
- Blood pressure readings
- Activity history (runs, cycles, swims, etc.)

**We take this seriously.** This project is designed to minimize risk at every layer.

## Built-In Protections

### 🔒 SafeGarmin Safety Lock

All destructive API operations are blocked by default:
- `delete_activity()` — blocked
- `delete_workout()` — blocked
- `delete_blood_pressure()` — blocked
- `delete_weigh_in()` — blocked
- `delete_weigh_ins()` — blocked
- `unschedule_workout()` — blocked

To perform any of these operations, you must explicitly use the raw `Garmin` class instead of `SafeGarmin`.

### 🔐 Credential Handling

- Credentials are **never hardcoded** in the project source
- The `.gitignore` excludes `.garminconnect/` and `.env` patterns
- Session tokens are stored locally at `~/.garminconnect/garmin_tokens.json`
- Tokens auto-refresh for ~1 year via Garmin's SSO (Garth) protocol

### 📡 No Third-Party Data Sharing

- All API calls go directly from your machine to `connect.garmin.com`
- No telemetry, analytics, or external logging
- No third-party servers receive your credentials or health data
- The sole dependency (`python-garminconnect`) communicates only with Garmin's own API

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it privately.

**Do NOT open a public GitHub issue** for security vulnerabilities.

### How to Report

1. **Email:** Open a GitHub issue with the label `security` and mark it as **confidential** (if your repo supports it), OR
2. **GitHub Security Advisory:** Use the "Report a vulnerability" link under the Security tab of this repository

Please include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **48 hours:** Acknowledgment of receipt
- **7 days:** Initial assessment and mitigation plan
- **30 days:** Fix deployed for supported versions

## Recommended User Practices

1. **Never commit credentials to version control** — use environment variables or config files excluded by `.gitignore`
2. **Use a dedicated Garmin account** for development/testing
3. **Review workout payloads** before uploading — the API sends exactly what you construct
4. **Keep dependencies updated** — `pip install --upgrade garminconnect` for the latest security fixes
5. **Run the self-test** (`python3 safe_garmin.py`) before automated operation to verify the safety lock

## Dependency Security

| Dependency | Version | Security |
|------------|---------|----------|
| [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) | ≥0.3.3 | MIT license, actively maintained by cyberjunky. Communicates exclusively with Garmin Connect's API over HTTPS. |

Dependencies are pinned in `pyproject.toml` with minimum versions. We recommend using exact version pins in production deployments.

## Security Audit History

| Date | Scope | Result |
|------|-------|--------|
| 2026-06-04 | Initial release — code review of SafeGarmin wrapper, credential flow, data transmission | ✅ No vulnerabilities found |

---

*Last updated: 2026-06-04*
