"""Tests for SafeGarmin safety lock."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PACKAGE = ROOT / "garmin_training_agent_manage"
SCRIPT = PACKAGE / "safe_garmin.py"
LEGACY_SCRIPT = ROOT / "safe_garmin.py"


def test_self_test_script_runs():
    """The self-test should exit 0 when all checks pass."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True,
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    assert result.returncode == 0


def test_legacy_shim_runs():
    """The root-level safe_garmin.py shim should also work."""
    result = subprocess.run(
        [sys.executable, str(LEGACY_SCRIPT)],
        capture_output=True, text=True,
    )
    print(result.stdout)
    assert result.returncode == 0
    assert "blocked" in result.stdout


def test_self_test_output_contains_blocked_markers():
    """Output should show blocked methods as ✓ and safe methods as ✓."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True,
    )
    assert "blocked" in result.stdout
    assert "accessible" in result.stdout
    assert "delete_activity" in result.stdout
    assert "delete_workout" in result.stdout
    assert "upload_running_workout" in result.stdout
    assert "get_workouts" in result.stdout


def test_blocked_methods_raise_error():
    """Test that blocked methods raise SafeGarminError."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("safe_garmin", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    obj = object.__new__(mod.SafeGarmin)

    blocked_methods = [
        "delete_activity",
        "delete_workout",
        "delete_blood_pressure",
        "delete_weigh_in",
        "delete_weigh_ins",
        "unschedule_workout",
    ]
    for method in blocked_methods:
        try:
            getattr(obj, method)()
            assert False, f"{method} should have raised SafeGarminError"
        except mod.SafeGarminError:
            pass  # Expected


def test_safe_methods_accessible():
    """Test that safe methods pass through to Garmin base class."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("safe_garmin", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    obj = object.__new__(mod.SafeGarmin)

    safe_methods = [
        "upload_running_workout",
        "upload_workout",
        "schedule_workout",
        "get_workouts",
        "get_activities",
        "login",
        "get_full_name",
    ]
    for method in safe_methods:
        assert hasattr(obj, method), f"{method} should be accessible"


def test_importable():
    """Module should be importable as a standalone module."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("safe_garmin", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "SafeGarmin")
    assert hasattr(mod, "SafeGarminError")


def test_blocked_methods_via_getattribute():
    """Test __getattribute__ interception works for blocked methods."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("safe_garmin", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    obj = object.__new__(mod.SafeGarmin)

    try:
        obj.delete_activity(42)
        assert False, "Should have raised SafeGarminError"
    except mod.SafeGarminError as e:
        assert "Deleting activities" in str(e)

    try:
        obj.unschedule_workout(99)
        assert False, "Should have raised SafeGarminError"
    except mod.SafeGarminError as e:
        assert "Unscheduling workouts" in str(e)


def test_package_import():
    """Test importing from the package works."""
    import importlib.util
    pkg_init = PACKAGE / "__init__.py"
    spec = importlib.util.spec_from_file_location("garmin_training_agent_manage", pkg_init)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "SafeGarmin")
    assert hasattr(mod, "SafeGarminError")
    assert hasattr(mod, "__version__")


def test_module_as_main():
    """Test python3 -m garmin_training_agent_manage works."""
    result = subprocess.run(
        [sys.executable, "-m", "garmin_training_agent_manage"],
        capture_output=True, text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0
    assert "blocked" in result.stdout
