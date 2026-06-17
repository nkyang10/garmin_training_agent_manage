"""Garmin Training Agent — Manage.

Push structured training plans to Garmin Connect programmatically,
with a safety-first SafeGarmin wrapper that blocks accidental deletions.

Usage:
    from garmin_training_agent_manage import SafeGarmin, SafeGarminError

    client = SafeGarmin("email", "password")
    client.login()
    result = client.upload_running_workout(workout)
    client.schedule_workout(result["workoutId"], "2026-06-10")
"""

from garmin_training_agent_manage.safe_garmin import SafeGarmin, SafeGarminError

__all__ = ["SafeGarmin", "SafeGarminError"]
__version__ = "1.0.0"
