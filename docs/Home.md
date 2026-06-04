# Welcome to the Garmin Training Agent Manage Wiki

## Quick Start

```bash
pip install garminconnect
```

```python
from safe_garmin import SafeGarmin

client = SafeGarmin("your@email.com", "your_password")
client.login()

# Upload a workout
result = client.upload_running_workout(workout)
client.schedule_workout(result["workoutId"], "2026-06-10")
```

## Resources

- [Main Repository](https://github.com/nkyang10/garmin_training_agent_manage)
- [Issue Tracker](https://github.com/nkyang10/garmin_training_agent_manage/issues)
- [PyPI: garminconnect](https://pypi.org/project/garminconnect/)
