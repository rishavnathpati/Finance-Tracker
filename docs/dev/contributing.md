# Contributing to Finance Tracker

Thank you for your interest in contributing to Finance Tracker! This document provides guidelines and instructions for contributing.

## Code Style and Standards

### Python Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Sort imports using [isort](https://pycqa.github.io/isort/)
- Maximum line length is 88 characters (Black default)

### Type Hints
- Use type hints for all function arguments and return values
- Use `Optional` for parameters that can be None
- Use `Union` for parameters that can be multiple types
- Follow [PEP 484](https://www.python.org/dev/peps/pep-0484/) guidelines

### Documentation
- Write docstrings for all modules, classes, and functions
- Follow [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for docstrings
- Keep documentation up to date with code changes
- Add comments for complex logic

## Development Process

### 1. Setting Up Development Environment
```bash
# Clone repository
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 2. Making Changes
1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following our code style guidelines

3. Run code quality checks:
```bash
# Format code
black src/ tests/
isort src/ tests/

# Run type checking
mypy src/

# Run linting
flake8 src/ tests/

# Run tests
pytest
```

4. Update documentation as needed

### 3. Submitting Changes

1. Commit your changes:
```bash
git add .
git commit -m "feat: your feature description"
```

2. Push to your fork:
```bash
git push origin feature/your-feature-name
```

3. Create a Pull Request:
   - Use a clear title and description
   - Reference any related issues
   - Include screenshots for UI changes
   - Update documentation if needed

## Pull Request Guidelines

### PR Title Format
Use conventional commits format:
- `feat: add new feature`
- `fix: resolve bug issue`
- `docs: update documentation`
- `test: add tests`
- `refactor: improve code structure`

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Tested manually

## Screenshots
(if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Added tests
- [ ] Updated documentation
- [ ] All tests passing
```

## Testing Guidelines

### Unit Tests
- Write tests for all new functionality
- Use pytest fixtures for common setup
- Mock external dependencies
- Aim for high test coverage

### Integration Tests
- Test interactions between components
- Test database operations
- Test GUI components

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_file.py

# Run with coverage report
pytest --cov=src tests/
```

## Documentation Guidelines

### Code Documentation
- Clear and concise docstrings
- Explain complex algorithms
- Document assumptions and edge cases
- Include examples for complex functions

### Project Documentation
- Keep README.md up to date
- Document new features
- Update configuration examples
- Add troubleshooting guides

## Git Workflow

### Branch Naming
- `feature/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation changes
- `refactor/`: Code improvements
- `test/`: Test additions or modifications

### Commit Messages
Follow conventional commits:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Example:
```
feat(transactions): add filtering by date range

- Added date range picker component
- Implemented filter logic in FinanceManager
- Updated tests

Fixes #123
```

## Code Review Process

### Reviewer Guidelines
- Check code style compliance
- Verify test coverage
- Review documentation updates
- Test functionality
- Provide constructive feedback

### Author Guidelines
- Respond to feedback promptly
- Make requested changes
- Update PR as needed
- Keep PR focused and small

## Getting Help

1. Check existing documentation
2. Search closed issues
3. Ask in discussions
4. Create a new issue

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
