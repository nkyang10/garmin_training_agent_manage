"""
Safe Garmin Connect wrapper

Disables all DELETE operations to prevent accidental data loss.
Use this instead of raw `garminconnect.Garmin` in production code.

Usage:
    from safe_garmin import SafeGarmin

    client = SafeGarmin("email", "password")
    client.login()

    # ✅ These still work: upload, schedule, get, etc.
    result = client.upload_running_workout(workout)
    client.schedule_workout(result["workoutId"], "2026-06-02")

    # ❌ These will raise SafeGarminError:
    client.delete_activity(123)        # Blocked!
    client.delete_workout(456)         # Blocked!
"""

from garminconnect import Garmin


class SafeGarminError(RuntimeError):
    """Raised when a blocked operation is attempted."""
    pass


class SafeGarmin(Garmin):
    """
    Garmin Connect client wrapper that blocks all destructive operations.

    Blocked methods will raise SafeGarminError with a clear message.
    """

    BLOCKED = {
        "delete_activity": "Deleting activities is disabled (SafeGarmin safety lock)",
        "delete_workout": "Deleting workouts is disabled (SafeGarmin safety lock)",
        "delete_blood_pressure": "Deleting blood pressure data is disabled (SafeGarmin safety lock)",
        "delete_weigh_in": "Deleting weigh-ins is disabled (SafeGarmin safety lock)",
        "delete_weigh_ins": "Deleting weigh-ins is disabled (SafeGarmin safety lock)",
        "unschedule_workout": "Unscheduling workouts is disabled (SafeGarmin safety lock)",
    }

    def __getattribute__(self, name):
        """Intercept blocked methods before they can execute."""
        blocked = object.__getattribute__(self, "BLOCKED")
        if name in blocked:
            raise SafeGarminError(blocked[name])
        return object.__getattribute__(self, name)

    # --- Method-level overrides for IDE autocomplete clarity ---

    def delete_activity(self, *args, **kwargs):
        raise SafeGarminError(self.BLOCKED["delete_activity"])

    def delete_workout(self, *args, **kwargs):
        raise SafeGarminError(self.BLOCKED["delete_workout"])

    def delete_blood_pressure(self, *args, **kwargs):
        raise SafeGarminError(self.BLOCKED["delete_blood_pressure"])

    def delete_weigh_in(self, *args, **kwargs):
        raise SafeGarminError(self.BLOCKED["delete_weigh_in"])

    def delete_weigh_ins(self, *args, **kwargs):
        raise SafeGarminError(self.BLOCKED["delete_weigh_ins"])

    def unschedule_workout(self, *args, **kwargs):
        raise SafeGarminError(self.BLOCKED["unschedule_workout"])


# Quick self-test
if __name__ == "__main__":
    print("🔒 SafeGarmin safety check:")
    blocked = [
        "delete_activity", "delete_workout",
        "delete_blood_pressure", "delete_weigh_in", "delete_weigh_ins",
        "unschedule_workout",
    ]
    safe = [
        "upload_running_workout", "upload_workout", "schedule_workout",
        "get_workouts", "get_activities", "login", "get_full_name",
    ]

    for method in blocked:
        try:
            obj = object.__new__(SafeGarmin)
            object.__getattribute__(obj, method)()
            print(f"  ❌ {method} — NOT blocked (BUG!)")
        except SafeGarminError:
            print(f"  ✅ {method} — blocked ✓")

    for method in safe:
        obj = object.__new__(SafeGarmin)
        if hasattr(obj, method):
            print(f"  ✅ {method} — accessible ✓")
        else:
            print(f"  ❌ {method} — MISSING!")
