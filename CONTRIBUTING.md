# Contributing to GLMReasoner

Thank you for your interest in contributing to GLMReasoner!

## Development Setup

1. Clone the repository
```bash
git clone https://github.com/gitstq/GLMReasoner.git
cd GLMReasoner
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -e ".[dev]"
```

4. Run tests
```bash
pytest
```

## Code Style

- Follow PEP 8
- Use Black for formatting
- Use isort for imports
- Write type hints where possible

## Commit Messages

We follow Conventional Commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/tooling changes

Example:
```
feat: add tree of thought reasoning strategy

Add support for tree of thought reasoning with branching paths
for exploring multiple solution approaches simultaneously.
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Ensure all tests pass
6. Submit a pull request

## Issues

- Use GitHub Issues for bug reports
- Include reproduction steps
- Specify your environment (Python version, OS, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
