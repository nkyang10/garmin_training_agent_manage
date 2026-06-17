#!/usr/bin/env python3
"""Basic usage examples for Garmin Training Agent Manage.

Run each example independently. None require a real Garmin Connect account
except Example 3 (upload), which needs credentials in environment variables.

Usage:
    python3 examples/basic_usage.py 1    # SafeGarmin safety lock demo
    python3 examples/basic_usage.py 2    # Self-test
    python3 examples/basic_usage.py 3    # Time-based easy run (needs GARMIN_* env vars)
    python3 examples/basic_usage.py 3 --dry-run  # Preview the workout JSON without uploading
"""

import json
import os
import sys
from pathlib import Path

# Add repo root to sys.path for direct script usage
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def example_1_safety_lock():
    """SafeGarmin blocks all delete operations."""
    from garmin_training_agent_manage import SafeGarmin, SafeGarminError

    client = SafeGarmin("dummy@example.com", "dummy_password")

    print("🔒 Safety lock demo:\n")

    # These will raise SafeGarminError (no credentials needed to trigger the block)
    for method_name in ["delete_activity", "delete_workout", "unschedule_workout"]:
        try:
            getattr(client, method_name)(123)
            print(f"  ❌ {method_name} — NOT blocked (BUG!)")
        except SafeGarminError as e:
            print(f"  ✅ {method_name} — blocked: {e}")

    # Safe methods are accessible (they'll fail with auth error, but that's expected)
    for method_name in ["upload_workout", "schedule_workout", "get_workouts"]:
        assert hasattr(client, method_name), f"{method_name} should exist"
        print(f"  ✅ {method_name} — accessible ✓")


def example_2_self_test():
    """Run the self-test (no credentials needed)."""
    from garmin_training_agent_manage.safe_garmin import main
    main()


def example_3_time_based_run(dry_run=False):
    """Create and schedule a time-based easy run.

    Requires GARMIN_EMAIL and GARMIN_PASSWORD environment variables.
    Use --dry-run to preview the workout JSON without uploading.
    """
    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")

    if not email or not password:
        print("❌ Set GARMIN_EMAIL and GARMIN_PASSWORD environment variables")
        sys.exit(1)

    from garminconnect.workout import (
        RunningWorkout, WorkoutSegment,
        create_warmup_step, create_cooldown_step, create_interval_step,
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
                    create_interval_step(900, step_order=2, target_type={
                        "workoutTargetTypeKey": "no.target"
                    }),
                    create_cooldown_step(300, step_order=3),
                ]
            )
        ]
    )

    if dry_run:
        print("📋 Dry-run — workout payload:")
        print(json.dumps(workout.model_dump(), indent=2))
        return

    from garmin_training_agent_manage import SafeGarmin

    client = SafeGarmin(email, password)
    client.login()

    result = client.upload_running_workout(workout)
    workout_id = result.get("workoutId", result.get("id"))
    print(f"✅ Uploaded workout ID: {workout_id}")

    from datetime import datetime, timedelta
    target_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    client.schedule_workout(str(workout_id), target_date)
    print(f"✅ Scheduled to {target_date}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    examples = {
        "1": example_1_safety_lock,
        "2": example_2_self_test,
        "3": lambda: example_3_time_based_run("--dry-run" in sys.argv),
    }

    fn = examples.get(sys.argv[1])
    if fn:
        fn()
    else:
        print(f"Unknown example: {sys.argv[1]}")
        sys.exit(1)
