# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Mandatory show-before-upload workflow for AI agents (For AI Agents section in README)
- Package layout (`garmin_training_agent_manage/`) with `__init__.py` and `__main__.py`
- `python3 -m garmin_training_agent_manage` entry point for self-test
- Executable examples (`examples/basic_usage.py`) with CLI runner — replaces usage.md
- GitHub Issue Templates: bug report + feature request
- Dependabot config for weekly pip updates
- CODE_OF_CONDUCT.md (Contributor Covenant v2.1)

### Changed
- `pyproject.toml`: added optional dev dependencies (pytest, ruff), Production/Stable classifier
- `pyproject.toml`: added package discovery config for new package layout
- `safe_garmin.py`: refactored self-test into `main()` function for importable use
- Root `safe_garmin.py` now a backward-compatible import shim
- Tests: updated for new package layout, added legacy shim test and `-m` entry-point test
- README: all import paths updated to `from garmin_training_agent_manage import SafeGarmin`

### Removed
- `examples/usage.md` — replaced by executable `examples/basic_usage.py`

## [1.0.0] - 2026-06-04

### Added
- SafeGarmin wrapper — blocks all `delete_*` and `unschedule_*` calls
- Full reference for `workoutTargetTypeId` (brute-force tested 1-10)
- Distance-based step support with auto-advance (`conditionTypeId=3`)
- Correct pace target format (`targetTypeId=6` + step-level m/s values)
- Working 6×800m + 6×600m track workout JSON example
- Mobile integration patterns (bookmarklet, backend proxy, OAuth2 PKCE)
- Step ordering gotcha documentation (API sorts by `stepOrder`)
- PUT modification gotcha (warmup/cooldown steps may be silently dropped)
- Comprehensive README with AI agent section
- CI pipeline (ruff lint + pytest matrix 3.8-3.12)
- pytest tests for SafeGarmin safety lock
