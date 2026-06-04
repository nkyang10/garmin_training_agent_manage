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

Then in Python:

```python
from safe_garmin import SafeGarmin

client = SafeGarmin("your@email.com", "your_password")
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

### CLI Usage

```bash
# SafeGarmin self-test (no API calls needed)
python3 safe_garmin.py
# → Prints ✓/✗ for each blocked vs allowed method
```

### Python API

```python
from safe_garmin import SafeGarmin, SafeGarminError

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
from safe_garmin import SafeGarmin

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

The full source is at [`safe_garmin.py`](safe_garmin.py) — 100 lines, no external deps beyond `garminconnect`.

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
| [`safe_garmin.py`](safe_garmin.py) | SafeGarmin wrapper source (100 LOC) |
| [`references/garmin-target-type-ids.md`](references/garmin-target-type-ids.md) | Brute-force results of all 10 targetTypeId values |
| [`references/interval-track-workout.json`](references/interval-track-workout.json) | Working 6×800m + 6×600m track session JSON |
| [`references/mobile-integration.md`](references/mobile-integration.md) | iOS backend, bookmarklet, and OAuth patterns |

## Data Source

This project depends on the [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) library (MIT License) by Ron Klinkien (cyberjunky), which wraps Garmin Connect's internal REST API.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

## Third-Party Notices

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution of bundled and referenced third-party works.
