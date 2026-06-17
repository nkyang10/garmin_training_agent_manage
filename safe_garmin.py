"""
Backward-compatible import shim.

This file is kept at the repo root so existing code doing
``from safe_garmin import SafeGarmin`` continues to work.

New code should import from the package instead:
    from garmin_training_agent_manage import SafeGarmin, SafeGarminError
"""

from garmin_training_agent_manage import SafeGarmin, SafeGarminError  # noqa: F401
from garmin_training_agent_manage.safe_garmin import main  # noqa: F401

if __name__ == "__main__":
    main()
