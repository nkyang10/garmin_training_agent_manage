# Garmin Workout Target Type ID Reference

Results of brute-force testing all `workoutTargetTypeId` values 1-10 against the Garmin Connect `/workout-service/workout` API (May 2026).

## Methodology

Each ID was tested with `upload_workout()` sending a single-step JSON payload:
```python
{"targetType": {"workoutTargetTypeId": TID, "workoutTargetTypeKey": "pace.zone"},
 "targetValueOne": 4.0, "targetValueTwo": 4.3}
```

The API response's `targetType.workoutTargetTypeKey` was then checked to see if the key was preserved.

## Results

| Tested ID | Given Key | API Response Key | Preserved? | Real Usage |
|-----------|-----------|-----------------|------------|------------|
| 2 | `pace.zone` | `power.zone` | ❌ Renamed | Power (cycling) |
| 5 | `pace.zone` | `speed.zone` | ❌ Renamed | Speed zones |
| **6** | **`pace.zone`** | **`pace.zone`** | **✅ Exact** | **Pace targets** |
| 7 | `pace.zone` | `grade` | ❌ Renamed | Grade/incline |
| 8 | `pace.zone` | `heart.rate.lap` | ❌ Renamed | Per-lap HR |
| 9 | `pace.zone` | `power.lap` | ❌ Renamed | Per-lap power |
| 10 | `pace.zone` | `power.3s` | ❌ Renamed | 3s power |

## Key Finding

The `garminconnect` library defines:
- `TargetType.NO_TARGET = 1`
- `TargetType.POWER = 2` (→ power.zone)
- `TargetType.CADENCE = 3`
- `TargetType.HEART_RATE = 4` (→ heart.rate.zone)
- `TargetType.SPEED = 5` (→ speed.zone)
- `TargetType.OPEN = 6`

But the Garmin API actually maps ID=6 to **pace.zone**, not "open". The library's `TargetType.OPEN` name is misleading — the API interprets the key string, not just the ID.

## Correct Pacing Call Format

```python
{
    "targetType": {
        "workoutTargetTypeId": 6,
        "workoutTargetTypeKey": "pace.zone"
    },
    "targetValueOne": 3.9,    # slower bound in m/s
    "targetValueTwo": 4.3     # faster bound in m/s
}
```

## Important

Step-level fields `targetValueOne` and `targetValueTwo` are the only reliable way to pass custom pace range values. Nested dictionaries inside `targetType` (like `paceRange`, `speedRange`, `heartRateZone`) are systematically stripped by the Garmin API's workout creation endpoint.

---

# Garmin Workout End Condition Type ID Reference

## Methodology

Each `conditionTypeId` was tested by sending a single-step JSON payload and checking whether the API preserved or normalized the key.

```python
{"endCondition": {"conditionTypeId": CID, "conditionTypeKey": KEY},
 "endConditionValue": 400.0}
```

## Results

| Tested ID | Given Key | API Response Key | Preserved? | Watch Behavior |
|-----------|-----------|-----------------|------------|----------------|
| 1 | `distance` | `lap.button` | ❌ Normalized | Manual — press Lap to advance |
| 1 | `lap.button` | `lap.button` | ✅ Exact | Manual — press Lap to advance |
| **3** | **`distance`** | **`distance`** | **✅ Exact** | **Auto-advance — GPS detects distance** |
| 3 | `lap.button` | `distance` | 🔄 Key swapped | Auto-advance |
| 8 | `distance` | `fixed.rest` | ❌ Renamed | Fixed rest period |

## Key Findings

- **`conditionTypeId=1` + `"lap.button"`** = Manual lap press (step advances when you press Lap)
- **`conditionTypeId=3` + `"distance"`** = Auto-advance by GPS distance (step advances automatically)
- The Garmin API normalizes `conditionTypeId=1` + `"distance"` to `"lap.button"` silently — the only way to get distance auto-advance is `conditionTypeId=3`

## Recommended Usage

```python
# Auto-advance (preferred for track workouts — GPS tracks distance)
{"conditionTypeId": 3, "conditionTypeKey": "distance"}

# Manual lap press (for pool swimming or when you want manual control)
{"conditionTypeId": 1, "conditionTypeKey": "lap.button"}
```
