# Usage Examples

## 1. SafeGarmin Safety Lock

```python
from safe_garmin import SafeGarmin, SafeGarminError

# All delete operations are blocked:
client = SafeGarmin("email", "password")
try:
    client.delete_workout(123)
except SafeGarminError as e:
    print(f"✅ Blocked: {e}")  # → "Deleting workouts is disabled"

# All upload and read operations work normally:
# client.upload_workout(...)
# client.schedule_workout(...)
# client.get_workouts()
```

## 2. Self-Test (No Credentials Needed)

```bash
python3 safe_garmin.py
```

Output:
```
🔒 SafeGarmin safety check:
  ✅ delete_activity — blocked ✓
  ✅ delete_workout — blocked ✓
  ✅ upload_running_workout — accessible ✓
  ✅ get_workouts — accessible ✓
```

## 3. Time-Based Easy Run

```python
from garminconnect.workout import (
    RunningWorkout, WorkoutSegment,
    create_warmup_step, create_interval_step, create_cooldown_step,
    create_repeat_group, create_recovery_step
)

workout = RunningWorkout(
    workoutName="Easy Run 5K",
    estimatedDurationInSecs=1800,
    workoutSegments=[
        WorkoutSegment(
            segmentOrder=1,
            sportType={"sportTypeId": 1, "sportTypeKey": "running"},
            workoutSteps=[
                create_warmup_step(600, step_order=1),
                create_interval_step(1200, step_order=2, target_type={
                    "workoutTargetTypeKey": "no.target"
                }),
                create_cooldown_step(300, step_order=3),
            ]
        )
    ]
)

result = client.upload_running_workout(workout)
print(f"Workout ID: {result['workoutId']}")
```

## 4. Distance-Based Track Session

See [`references/interval-track-workout.json`](../references/interval-track-workout.json) for a complete 6×800m + 6×600m example with:

- Lap-button end conditions (manual advance)
- Pace targets with m/s values
- 90-second recovery jogs
- Warmup and cooldown
