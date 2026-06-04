# Pace Targets Reference

## Correct Format

```python
{
    "targetType": {
        "workoutTargetTypeId": 6,
        "workoutTargetTypeKey": "pace.zone"
    },
    "targetValueOne": 3.704,   # slower bound (m/s)
    "targetValueTwo": 3.846    # faster bound (m/s)
}
```

## m/s Conversion Table

| Pace | m/s |
|------|-----|
| 5:00/km | 3.333 |
| 4:35/km | 3.636 |
| 4:15/km | 3.922 |
| 4:00/km | 4.167 |
| 3:45/km | 4.444 |
| 3:30/km | 4.762 |

Formula: `m/s = 1000 / (minutes * 60 + seconds)`

## Common Mistakes

- ❌ `workoutTargetTypeId=2` → silently converts to power.zone
- ❌ Nested `paceRange` dict → silently dropped
- ❌ `pace.range` key → silently dropped
- ✅ `workoutTargetTypeId=6` + `pace.zone` + step-level `targetValueOne/Two`
