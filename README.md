<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/banner-dark.svg">
  <img src=".github/banner-light.svg" width="600">
</picture>

# Garmin Training Agent — Manage

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/nkyang10/garmin_training_agent_manage/actions/workflows/ci.yml/badge.svg)](https://github.com/nkyang10/garmin_training_agent_manage/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/badge/pip-install-006dad.svg)](https://pypi.org/project/garminconnect/)

> Push structured training plans to Garmin Connect programmatically — with a safety-first `SafeGarmin` wrapper that blocks accidental deletions.

## Features

- ✅ **Upload running workouts** — time-based and distance-based intervals, warmup, cooldown, repeat groups
- ✅ **Schedule to calendar** — one workout or many, any date
- ✅ **Update existing workouts** — via PUT or delete+recreate pattern
- ✅ **SafeGarmin wrapper** — blocks all `delete_*` and `unschedule_*` calls to prevent accidental data loss
- ✅ **Correct pace targets** — battle-tested `workoutTargetTypeId=6` approach with m/s conversion
- ✅ **Distance auto-advance** — GPS-based step progression (`conditionTypeId=3`)
- ✅ **Working JSON examples** — 6x800m + 6x600m track session
- ✅ **Mobile integration patterns** — iOS bookmarklet, backend proxy, OAuth2 PKCE
- ✅ **Full reference** — all 10 `workoutTargetTypeId` values brute-force tested against Garmin's API

## Quick Start

```bash
pip install garminconnect
```

Then in Python (use environment variables — never hardcode credentials):

```python
import os
from garmin_training_agent_manage import SafeGarmin

client = SafeGarmin(
    os.environ["GARMIN_EMAIL"],
    os.environ["GARMIN_PASSWORD"]
)
client.login()

# Create a simple 20-minute easy run
from garminconnect.workout import (
    RunningWorkout, WorkoutSegment,
    create_warmup_step, create_interval_step, create_cooldown_step
)

workout = RunningWorkout(
    workoutName="Easy Run 20min",
    estimatedDurationInSecs=1200,
    workoutSegments=[WorkoutSegment(
        segmentOrder=1,
        sportType={"sportTypeId": 1, "sportTypeKey": "running"},
        workoutSteps=[create_warmup_step(300, 1), create_interval_step(900, 2)]
    )]
)
result = client.upload_running_workout(workout)

# Schedule it
client.schedule_workout(result["workoutId"], "2026-06-10")
print(f"✅ Workout scheduled! ID: {result['workoutId']}")
```

## For AI Agents

This project is designed to be used by other AI coding agents.

### ⚠️ Mandatory Workflow: Show Before Upload

**CRITICAL RULE:** When an AI agent is managing workouts for a user, the workflow MUST be:

1. Plan workouts based on user's goals and schedule
2. Present the complete plan (dates, workout names, step details, pace targets) for user review
3. Wait for explicit user confirmation ("放上去" / "ok" / "confirm")
4. Only then upload + schedule to Garmin Connect

Never upload or schedule workouts directly without user approval. This is a hard requirement.

### CLI Usage

```bash
# SafeGarmin self-test (no API calls needed)
python3 -m garmin_training_agent_manage
# → Prints ✓/✗ for each blocked vs allowed method
```

### Python API

```python
from garmin_training_agent_manage import SafeGarmin, SafeGarminError

client = SafeGarmin("email", "password")
client.login()                          # → None (saves token to ~/.garminconnect/)

# Upload methods
result = client.upload_workout({...})   # → dict {workoutId, ...}
result = client.upload_running_workout(workout)  # → dict

# Scheduling
client.schedule_workout("12345", "2026-06-10")  # → None

# Reading
workouts = client.get_workouts()                # → list[dict]
detail = client.get_workout_by_id("12345")      # → dict

# SafeGarmin blocks:
client.delete_workout(123)  # → raises SafeGarminError 🛡️
```

### Exit Codes

- `0` — Self-test passed (all blocked methods blocked, all safe methods accessible)
- `1` — Self-test failed (a blocked method was NOT blocked, or a safe method is missing)

### Dependencies

- **garminconnect** (PyPI, MIT) — the underlying Garmin Connect API wrapper by [cyberjunky](https://github.com/cyberjunky/python-garminconnect)
- Pure Python 3.8+ — no other dependencies for `safe_garmin.py` itself

## SafeGarmin Safety Lock

Always use `SafeGarmin` instead of raw `Garmin` to prevent accidental data loss:

```python
from garmin_training_agent_manage import SafeGarmin

client = SafeGarmin("email", "password")
client.login()

# These are BLOCKED:
#   client.delete_activity(123)        → SafeGarminError
#   client.delete_workout(456)         → SafeGarminError
#   client.unschedule_workout(789)     → SafeGarminError

# These work normally:
#   client.upload_workout(...)
#   client.schedule_workout(...)
#   client.get_workouts()
```

The full source is at [`garmin_training_agent_manage/safe_garmin.py`](garmin_training_agent_manage/safe_garmin.py) — 100 lines, no external deps beyond `garminconnect`.

## Distance-Based Steps (Track Workouts)

For 400m, 800m, 300m intervals, use raw `ExecutableStep` objects:

```python
from garminconnect.workout import ExecutableStep, RepeatGroup, RunningWorkout, WorkoutSegment

# Auto-advance by GPS distance (conditionTypeId=3)
step = ExecutableStep(
    type="ExecutableStepDTO",
    stepOrder=1,
    stepType={"stepTypeId": 3, "stepTypeKey": "interval", "displayOrder": 3},
    endCondition={"conditionTypeId": 3, "conditionTypeKey": "distance"},
    endConditionValue=800.0,
    targetType={"workoutTargetTypeId": 6, "workoutTargetTypeKey": "pace.zone"},
    targetValueOne=3.704,   # 4:30/km in m/s
    targetValueTwo=3.846,   # 4:20/km in m/s
    description="800m @ 4:25/km"
)
```

Full working example: [`references/interval-track-workout.json`](references/interval-track-workout.json)

## Pace Target Reference

The Garmin API uses `workoutTargetTypeId=6` with `pace.zone` key for pace targets. Values must be in **meters per second (m/s)** at the **step level**:

| Pace | m/s | Pace | m/s |
|------|-----|------|-----|
| 5:00/km | 3.333 | 4:00/km | 4.167 |
| 4:35/km | 3.636 | 3:45/km | 4.444 |
| 4:15/km | 3.922 | 3:30/km | 4.762 |
| 4:05/km | 4.082 | 3:10/km | 5.263 |

Formula: `m/s = 1000 / (minutes × 60 + seconds)`

**Do NOT use:** `pace.range` (nested dict), `speed.range`, or `workoutTargetTypeId` other than 6 — the API silently drops or remaps these values.

## Mobile Integration

Reference architecture patterns in [`references/mobile-integration.md`](references/mobile-integration.md):

- **iOS App → Python Backend → Garmin API** — reuse SafeGarmin on a server
- **Bookmarklet** (easiest) — JS bookmarklet on connect.garmin.com, no backend needed
- **iOS Direct OAuth2 PKCE** — native Swift, no server dependency

## References

| File | Description |
|------|-------------|
| [`garmin_training_agent_manage/safe_garmin.py`](garmin_training_agent_manage/safe_garmin.py) | SafeGarmin wrapper source (100 LOC) |
| [`references/garmin-target-type-ids.md`](references/garmin-target-type-ids.md) | Brute-force results of all 10 targetTypeId values |
| [`references/interval-track-workout.json`](references/interval-track-workout.json) | Working 6×800m + 6×600m track session JSON |
| [`references/mobile-integration.md`](references/mobile-integration.md) | iOS backend, bookmarklet, and OAuth patterns |

## Data Source

This project depends on the [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) library (MIT License) by Ron Klinkien (cyberjunky), which wraps Garmin Connect's internal REST API.

## Security & Data Privacy

Your Garmin account credentials grant access to personal health data — heart rate, sleep, location history, body composition, and more. This project is designed to **minimize risk** and be transparent about data handling.

### What Data Is Sent to Garmin

Only the workout payload you explicitly construct:
| Field | Example | Purpose |
|-------|---------|---------|
| `workoutName` | `"Easy Run 5K"` | Workout label on your watch |
| `workoutSegments` | Step definitions | Warmup, intervals, cooldown structure |
| `estimatedDurationInSecs` | `1800` | Total workout time estimate |
| `sportType` | `{"sportTypeId": 1}` | Running, cycling, swimming, etc. |

No location data, heart rate history, or any other personal health data is ever read or transmitted by this tool.

### What Data Stays on Your Machine

| Data | Location | Detail |
|------|----------|--------|
| Session token | `~/.garminconnect/garmin_tokens.json` | Auto-generated by garminconnect after login; valid ~1 year |
| Workout JSON (local copies) | Your own scripts / files | You control what you save |

**Credentials are never stored by this project** — the `garminconnect` library handles token persistence automatically.

### How Credentials Are Handled

```python
# ❌ Never hardcode credentials in scripts
client = SafeGarmin("my@email.com", "my_password")  # BAD — leaks in version control

# ✅ Use environment variables
import os
client = SafeGarmin(
    os.environ["GARMIN_EMAIL"],
    os.environ["GARMIN_PASSWORD"]
)

# ✅ Or load from a config file NOT tracked by git
# config.toml (add config.toml to .gitignore!)
```

The `.gitignore` in this repo already excludes `.garminconnect/` and `.env` patterns to prevent accidental commits of credential files.

### SafeGarmin: Your Safety Net

The `SafeGarmin` wrapper (this project's core contribution) prevents accidental data loss by blocking all destructive API operations:

- ❌ `delete_activity()` — blocked
- ❌ `delete_workout()` — blocked
- ❌ `delete_blood_pressure()` — blocked
- ❌ `delete_weigh_in()` — blocked
- ❌ `unschedule_workout()` — blocked

If you need to delete data, you must explicitly use the raw `Garmin` class — a deliberate, conscious action that prevents accidents during automated or AI-driven operation.

### Third-Party Data Sharing

**This project does not send data to any third-party service.** All API calls go directly from your machine to `connect.garmin.com` (Garmin's official API endpoint). No telemetry, no analytics, no external logging.

The only external dependency — [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) (MIT) — communicates exclusively with Garmin Connect's own API.

### Recommended Practices

1. **Use environment variables** for credentials — never hardcode them
2. **Add `.garminconnect/` to `.gitignore`** (already done in this repo)
3. **Run `safe_garmin.py` self-test** before any API call to verify the safety lock is active
4. **Review workout JSON before uploading** — the library sends exactly what you construct
5. **Schedule workouts in the near future** — avoid creating calendar entries years ahead
6. **Use a dedicated Garmin account** if testing extensively, rather than your primary training account

### Reporting a Vulnerability

See [SECURITY.md](SECURITY.md) for our vulnerability disclosure policy.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

## Third-Party Notices

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution of bundled and referenced third-party works.
