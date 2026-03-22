# Chapter 10: Robustness (Items 83–92)

This is a new chapter in the 3rd edition, focused on writing code that doesn't break.

## Exception Handling

### Catch specific exceptions, never bare except
```python
# Bad: Catches KeyboardInterrupt, SystemExit, everything
try:
    process(data)
except:
    pass

# Bad: Still too broad
try:
    process(data)
except Exception:
    log("something went wrong")

# Good: Catch what you can handle
try:
    result = parse(raw_input)
except (ValueError, json.JSONDecodeError) as e:
    return default_result(error=str(e))
```

### Minimize try block scope
Only wrap the specific operation that can raise, not the entire function body:
```python
# Bad: Which line raised?
try:
    data = load_file(path)
    parsed = parse(data)
    result = transform(parsed)
    save(result)
except FileNotFoundError:
    ...

# Good: Narrow scope
try:
    data = load_file(path)
except FileNotFoundError:
    return None

parsed = parse(data)
result = transform(parsed)
save(result)
```

### Use try/except/else/finally correctly
```python
try:
    f = open(path)
except FileNotFoundError:
    handle_missing()
else:
    # Only runs if no exception — put success logic here
    data = f.read()
finally:
    # Always runs — cleanup
    ...
```
The `else` clause prevents accidentally catching exceptions from the success path.

### Define exception hierarchies for libraries
```python
class MyLibraryError(Exception):
    """Root exception for mylib."""

class ConfigError(MyLibraryError):
    """Configuration is invalid."""

class NetworkError(MyLibraryError):
    """Network operation failed."""
```
Callers can catch `MyLibraryError` for broad handling, or specific subclasses
for targeted recovery.

## Defensive Patterns

### Validate at boundaries, trust internally
```python
# Public API boundary — validate
def create_user(name: str, age: int) -> User:
    if not name.strip():
        raise ValueError("name must not be empty")
    if age < 0 or age > 150:
        raise ValueError(f"invalid age: {age}")
    return _build_user(name.strip(), age)

# Internal function — trust the data
def _build_user(name: str, age: int) -> User:
    return User(name=name, age=age)  # No validation here
```

### Use assert for development invariants
```python
def process_batch(items: list[Item]) -> None:
    assert len(items) > 0, "Empty batch should have been filtered upstream"
    assert all(item.is_valid for item in items), "Invalid items in batch"
    ...
```
`assert` statements are removed when Python runs with `-O` (optimize flag).
Never use them for input validation in production code.

### Context managers for guaranteed cleanup
```python
from contextlib import contextmanager

@contextmanager
def temporary_directory():
    path = create_temp_dir()
    try:
        yield path
    finally:
        shutil.rmtree(path)
```

### warnings for deprecation and migration
```python
import warnings

def old_api(x):
    warnings.warn(
        "old_api() is deprecated, use new_api() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_api(x)
```

## Graceful Degradation

### Use fallback chains
```python
def get_config(key: str) -> str:
    # Try sources in priority order
    if (val := os.environ.get(key)):
        return val
    if (val := config_file.get(key)):
        return val
    if (val := DEFAULTS.get(key)):
        return val
    raise ConfigError(f"No value for {key}")
```

### Retry with exponential backoff
```python
import time

def retry(func, max_attempts: int = 3, base_delay: float = 1.0):
    for attempt in range(max_attempts):
        try:
            return func()
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))
```

## Key Takeaways
- Catch specific exceptions with narrow try blocks
- Use `else` clause to separate success path from exception handling
- Define root exceptions for libraries to insulate callers
- Validate at public API boundaries, use asserts for internal invariants
- `contextmanager` for resource cleanup, `warnings` for migration
- Build fallback chains and retry logic for resilient systems
