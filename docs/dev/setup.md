# Development Setup Guide

## Prerequisites

- Python 3.9 or higher
- Git
- pip (Python package installer)
- SQLite3

## Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Additional development dependencies
```

## Development Tools

### 1. Code Quality Tools

- **Black**: Code formatter
  ```bash
  black src/ tests/
  ```

- **isort**: Import sorter
  ```bash
  isort src/ tests/
  ```

- **flake8**: Code linter
  ```bash
  flake8 src/ tests/
  ```

- **mypy**: Type checker
  ```bash
  mypy src/
  ```

### 2. Testing

- **pytest**: Test runner
  ```bash
  # Run all tests
  pytest

  # Run with coverage report
  pytest --cov=src tests/

  # Run specific test file
  pytest tests/test_finance_manager.py
  ```

### 3. Database Management

- Initialize database:
  ```bash
  python -m src.utils.db_utils --init
  ```

- Reset database:
  ```bash
  python -m src.utils.db_utils --reset
  ```

## Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following these guidelines:
   - Follow PEP 8 style guide
   - Add type hints to all functions
   - Write docstrings for all modules, classes, and functions
   - Add unit tests for new functionality
   - Update documentation as needed

3. Run quality checks:
```bash
# Format code
black src/ tests/
isort src/ tests/

# Run linting and type checking
flake8 src/ tests/
mypy src/

# Run tests
pytest
```

4. Commit your changes:
```bash
git add .
git commit -m "feat: your feature description"
```

5. Push your changes and create a pull request:
```bash
git push origin feature/your-feature-name
```

## Project Structure

```
finance-tracker/
├── src/                 # Source code
│   ├── cli/            # Command-line interface
│   ├── core/           # Business logic
│   ├── gui/            # GUI components
│   ├── models/         # Database models
│   └── utils/          # Utilities
├── tests/              # Test files
├── docs/               # Documentation
└── scripts/            # Development scripts
```

## Configuration

1. Create a local configuration file:
```bash
cp config/default_config.py config/local_config.py
```

2. Set up environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` with your local settings

## Common Development Tasks

### Adding a New Feature

1. Create feature branch
2. Update database models if needed
3. Add business logic in core/
4. Add GUI components in gui/
5. Add tests
6. Update documentation
7. Submit pull request

### Debugging

1. Use logging:
```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.debug("Debug message")
```

2. Use PyQt6's debug tools:
   - Widget Inspector
   - Signal/Slot Debugger

3. Use SQLAlchemy's echo mode:
```python
engine = create_engine(DATABASE_URL, echo=True)
```

### Performance Profiling

1. Use cProfile:
```bash
python -m cProfile -o output.prof src/main.py
```

2. Analyze with snakeviz:
```bash
snakeviz output.prof
```

## Troubleshooting

### Common Issues

1. **Database errors**
   - Check database connection
   - Reset database: `python -m src.utils.db_utils --reset`

2. **GUI issues**
   - Check PyQt6 installation
   - Verify widget hierarchy

3. **Import errors**
   - Verify PYTHONPATH
   - Check virtual environment activation

### Getting Help

1. Check existing documentation in docs/
2. Search GitHub issues
3. Ask in the development channel
4. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details
