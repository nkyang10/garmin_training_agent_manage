# Contributing

Thanks for your interest in contributing to Garmin Training Agent Manage!

## How to Contribute

1. **Fork the repo** on GitHub
2. **Create a branch** (`git checkout -b feature/my-feature`)
3. **Make your changes**
4. **Test** — `python -m pytest tests/ -v`
5. **Lint** — `pip install ruff && ruff check .`
6. **Commit** with descriptive messages
7. **Push** to your fork
8. **Open a Pull Request**

## Code Style

- Python 3.8+ compatible
- Follow PEP 8 — ruff will catch violations
- Type hints are encouraged but not required
- Docstrings for public methods

## Testing

```bash
python -m pytest tests/ -v
```

Tests should NOT require a real Garmin Connect account. Mock external calls where needed.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
