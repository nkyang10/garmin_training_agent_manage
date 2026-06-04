# SafeGarmin Reference

## Overview

`SafeGarmin` is a safety wrapper around the `garminconnect.Garmin` class that blocks all destructive operations.

## Blocked Methods

| Method | Reason |
|--------|--------|
| `delete_activity()` | Prevents accidental activity deletion |
| `delete_workout()` | Prevents accidental workout deletion |
| `delete_blood_pressure()` | Prevents data loss |
| `delete_weigh_in()` | Prevents data loss |
| `delete_weigh_ins()` | Prevents data loss |
| `unschedule_workout()` | Prevents unintended unscheduling |

## Usage

```python
from safe_garmin import SafeGarmin, SafeGarminError

client = SafeGarmin("email", "password")
client.login()

try:
    client.delete_workout(123)
except SafeGarminError as e:
    print(f"Blocked: {e}")
```

## Self-Test

Run `python3 safe_garmin.py` for a no-credentials self-test.
