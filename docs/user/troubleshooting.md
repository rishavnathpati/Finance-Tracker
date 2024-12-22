# Troubleshooting Guide

This guide covers common issues and their solutions.

## Installation Issues

### Python Version Error
**Problem**: Error about Python version compatibility
**Solution**:
1. Check your Python version:
```bash
python --version
```
2. Install Python 3.9 or higher from [python.org](https://python.org)
3. Ensure you're using the correct Python version:
```bash
python3 --version  # On macOS/Linux
py -3 --version    # On Windows
```

### Dependency Installation Fails
**Problem**: pip install errors
**Solution**:
1. Upgrade pip:
```bash
python -m pip install --upgrade pip
```
2. Install dependencies one by one to identify problematic package:
```bash
pip install sqlalchemy
pip install PyQt6
```
3. Check for system-specific requirements:
   - Windows: Visual C++ build tools
   - Linux: python3-dev, build-essential
   - macOS: Command Line Tools

## Application Launch Issues

### Application Won't Start
**Problem**: Error when launching application
**Solution**:
1. Check Python path:
```bash
echo $PYTHONPATH  # On macOS/Linux
echo %PYTHONPATH% # On Windows
```
2. Verify database file exists:
```bash
ls finance_tracker.db
```
3. Check logs in logs/app.log

### GUI Doesn't Display
**Problem**: No window appears or GUI elements missing
**Solution**:
1. Verify PyQt6 installation:
```bash
python -c "import PyQt6"
```
2. Check system requirements:
   - X11 on Linux
   - Working display server
3. Try running with debug output:
```bash
python src/main.py --debug
```

## Database Issues

### Database Connection Error
**Problem**: Cannot connect to database
**Solution**:
1. Check database file permissions:
```bash
ls -l finance_tracker.db
```
2. Reset database:
```bash
python -m src.utils.db_utils --reset
```
3. Verify SQLite installation:
```bash
sqlite3 --version
```

### Data Import Fails
**Problem**: Cannot import transactions
**Solution**:
1. Check file format:
   - CSV: Verify column separators
   - QIF: Check date format
   - OFX: Validate XML structure
2. Try sample import file from docs/examples/
3. Use import validation:
```bash
python -m src.utils.data_manager --validate import_file.csv
```

### Data Corruption
**Problem**: Database shows incorrect data
**Solution**:
1. Restore from backup:
```bash
python -m src.utils.data_manager --restore latest
```
2. Check transaction logs:
```bash
python -m src.utils.data_manager --check-integrity
```
3. Export data before resetting:
```bash
python -m src.utils.data_manager --export backup.csv
```

## Performance Issues

### Slow Transaction Loading
**Problem**: Transaction list takes long to load
**Solution**:
1. Check database size:
```bash
ls -lh finance_tracker.db
```
2. Optimize database:
```bash
python -m src.utils.db_utils --optimize
```
3. Clear old data:
```bash
python -m src.utils.data_manager --archive-old
```

### Reports Generation Slow
**Problem**: Reports take long to generate
**Solution**:
1. Limit date range
2. Reduce chart complexity
3. Update database indices:
```bash
python -m src.utils.db_utils --update-indices
```

## Feature Issues

### Categories Not Showing
**Problem**: Missing transaction categories
**Solution**:
1. Reset default categories:
```bash
python -m src.utils.data_manager --reset-categories
```
2. Check category permissions
3. Verify category database table:
```bash
python -m src.utils.db_utils --check-tables
```

### Charts Not Updating
**Problem**: Dashboard charts don't reflect new data
**Solution**:
1. Refresh dashboard manually
2. Clear chart cache:
```bash
python -m src.utils.data_manager --clear-cache
```
3. Check data update events

## Configuration Issues

### Settings Not Saving
**Problem**: Application settings don't persist
**Solution**:
1. Check config file permissions:
```bash
ls -l config/config.json
```
2. Reset configuration:
```bash
python -m src.utils.config_manager --reset
```
3. Verify config directory exists:
```bash
mkdir -p config
```

### Currency Display Issues
**Problem**: Incorrect currency symbols or formatting
**Solution**:
1. Check locale settings
2. Update currency configuration:
```bash
python -m src.utils.config_manager --update-locale
```
3. Reset currency format:
```bash
python -m src.utils.config_manager --reset-currency
```

## System-Specific Issues

### Windows
1. **Path Issues**:
   - Use correct path separators
   - Check %APPDATA% permissions
   - Verify user permissions

2. **Display Issues**:
   - Update graphics drivers
   - Check Windows scaling settings
   - Verify PyQt6 installation

### macOS
1. **Permission Issues**:
   - Check Application Security settings
   - Verify file permissions
   - Allow Python in Security & Privacy

2. **M1/M2 Compatibility**:
   - Use Python 3.9+ arm64 build
   - Install Rosetta 2 if needed
   - Check architecture-specific dependencies

### Linux
1. **Display Issues**:
   - Install required X11 libraries
   - Check Qt dependencies
   - Verify display server

2. **Permission Issues**:
   - Check file ownership
   - Verify group permissions
   - Set correct SELinux context

## Getting Help

### Debug Information
Gather debug info:
```bash
python -m src.utils.error_handler --debug-info
```

### Log Files
Check logs:
1. Application log: logs/app.log
2. Error log: logs/error.log
3. Debug log: logs/debug.log

### Support Channels
1. GitHub Issues
2. Documentation Wiki
3. Community Forum
4. Email Support
