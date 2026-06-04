# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
