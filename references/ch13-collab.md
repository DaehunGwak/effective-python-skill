# Chapter 13–14: Collaboration (Items 116–125)

## Finding and Managing Dependencies

### Use pip and PyPI responsibly
- Pin exact versions in `requirements.txt` for applications: `requests==2.31.0`
- Use ranges in `pyproject.toml` for libraries: `requests>=2.28,<3`
- Use `uv` or `pip-tools` for dependency resolution and lockfiles
- Prefer well-maintained packages with active communities

### Virtual environments are mandatory
```bash
# Modern approach with uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Or classic venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Never install packages globally. Every project gets its own virtual environment.

## Documentation

### Write docstrings for every public function, class, and module
```python
def calculate_distance(
    origin: tuple[float, float],
    destination: tuple[float, float],
) -> float:
    """Calculate the great-circle distance between two GPS coordinates.

    Uses the Haversine formula. Coordinates are (latitude, longitude) in degrees.

    Args:
        origin: Starting point as (lat, lon).
        destination: End point as (lat, lon).

    Returns:
        Distance in kilometers.

    Raises:
        ValueError: If coordinates are outside valid ranges.
    """
```

### Docstring conventions
- First line: One-sentence summary (imperative mood: "Calculate", not "Calculates")
- Blank line after summary for longer docstrings
- Args, Returns, Raises sections (Google style or NumPy style — pick one, be consistent)
- Module-level docstrings describe the module's purpose
- Class docstrings describe behavior, not implementation

## Package Structure

### Use packages to organize modules
```
myproject/
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py      # Public API
│       ├── core.py
│       ├── models.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
└── tests/
    ├── conftest.py
    └── test_core.py
```

### Define explicit public APIs in __init__.py
```python
# mypackage/__init__.py
from mypackage.core import process, transform
from mypackage.models import User, Config

__all__ = ["process", "transform", "User", "Config"]
```
This controls what `from mypackage import *` exports and documents the intended
public interface.

### Module-scoped code for configuration
Use module-level code to configure deployment-specific behavior:
```python
# config.py
import os

ENVIRONMENT = os.environ.get("APP_ENV", "development")

if ENVIRONMENT == "production":
    DATABASE_URL = os.environ["DATABASE_URL"]
    DEBUG = False
else:
    DATABASE_URL = "sqlite:///dev.db"
    DEBUG = True
```

## Error Handling for Libraries

### Define a root exception for your library
```python
# mylib/exceptions.py
class MyLibError(Exception):
    """Base exception for mylib."""

class ConnectionError(MyLibError):
    """Failed to connect to the service."""

class AuthError(MyLibError):
    """Authentication failed."""
```
This lets callers catch all library errors with `except MyLibError` while still
allowing specific handling for individual error types.

### Break circular dependencies
Circular imports are a design smell. Solutions in order of preference:
1. **Restructure**: Move shared code to a new module
2. **Import at use-time**: Move the import inside the function that needs it
3. **Use `TYPE_CHECKING`**: Import only for type hints
```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypackage.models import User

def process(user: User) -> None:  # Type hint works, no circular import
    ...
```

## Static Analysis and Type Checking

### Use typing to catch bugs before runtime
```python
# pyproject.toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
```

### Progressive typing
Don't try to type everything at once. Start with:
1. Public API functions
2. Complex internal functions
3. Gradually tighten with `mypy --strict`

### Use `warnings` for API migration
```python
import warnings

def old_function():
    warnings.warn(
        "old_function is deprecated, use new_function instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_function()
```

## Key Takeaways
- Virtual environments for every project, pinned deps for apps
- Docstrings on all public APIs (Google/NumPy style, pick one)
- `__init__.py` + `__all__` to define explicit public interfaces
- Root exception class for libraries
- Break circular imports via restructuring or TYPE_CHECKING
- Progressive typing with mypy, start with public APIs
- `warnings` for deprecation and migration paths
