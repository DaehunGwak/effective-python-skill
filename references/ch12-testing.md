# Chapter 12: Testing and Debugging (Items 104–115)

## Testing Philosophy

### Write tests for every function and class
Tests are documentation that is always up to date. They describe what the code
is supposed to do and catch regressions. If it's not tested, it doesn't work.

### Use pytest, not unittest
pytest is the standard in modern Python. Its advantages:
- Plain `assert` instead of `self.assertEqual` — more readable, better error messages
- Fixtures over setUp/tearDown — composable, reusable, explicit
- Parameterization for testing multiple inputs concisely
- Rich plugin ecosystem (pytest-cov, pytest-mock, pytest-asyncio)

```python
# Good: pytest style
def test_parse_valid_input():
    result = parse("42")
    assert result == 42

def test_parse_invalid_input():
    with pytest.raises(ValueError, match="invalid"):
        parse("not_a_number")
```

### Use fixtures for test dependencies
```python
import pytest

@pytest.fixture
def db_connection():
    conn = create_test_db()
    yield conn
    conn.close()

@pytest.fixture
def sample_user(db_connection):
    return create_user(db_connection, name="test")

def test_user_login(sample_user):
    assert sample_user.can_login()
```

### Parameterize to avoid repetition
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("", ""),
    ("123", "123"),
    ("café", "CAFÉ"),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

## Test Design

### Test behavior, not implementation
Tests should describe what the code does, not how it does it:
```python
# Bad: Tests implementation details
def test_cache_uses_dict():
    cache = Cache()
    assert isinstance(cache._store, dict)

# Good: Tests behavior
def test_cache_returns_stored_value():
    cache = Cache()
    cache.set("key", "value")
    assert cache.get("key") == "value"
```

### Use mocking sparingly and strategically
Mock external boundaries (HTTP calls, databases, file systems), not internal code:
```python
# Good: Mock the external boundary
def test_fetch_user(mocker):
    mocker.patch("myapp.http.get", return_value={"name": "Alice"})
    user = fetch_user(42)
    assert user.name == "Alice"

# Bad: Mocking internal implementation
def test_process(mocker):
    mocker.patch("myapp.internal._helper", return_value=42)  # Too coupled
```

### Arrange-Act-Assert pattern
```python
def test_transfer():
    # Arrange
    source = Account(balance=100)
    target = Account(balance=50)

    # Act
    transfer(source, target, amount=30)

    # Assert
    assert source.balance == 70
    assert target.balance == 80
```

## Debugging

### Use breakpoint() for interactive debugging
```python
def complex_function(data):
    intermediate = transform(data)
    breakpoint()  # Drops into pdb (or configured debugger)
    return finalize(intermediate)
```
Set `PYTHONBREAKPOINT=0` to disable all breakpoints in production.

### Use repr() for unambiguous debug output
```python
# Ambiguous
print(f"value: {x}")      # "value: None" — is it a string "None" or NoneType?

# Unambiguous
print(f"value: {x!r}")    # "value: None" vs "value: 'None'"
```

### Use logging over print
```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Processing item %s", item_id)
logger.info("Batch complete: %d items", count)
logger.warning("Retry %d/%d for %s", attempt, max_attempts, url)
logger.error("Failed to process: %s", error, exc_info=True)
```
Configure logging at the application entry point, not in library code.

## Test Coverage

### Aim for high coverage on critical paths
- 100% coverage doesn't mean no bugs — but 0% coverage guarantees them
- Focus coverage on business logic, not boilerplate
- Use `pytest-cov` to measure: `pytest --cov=myapp --cov-report=term-missing`
- Branch coverage (`--cov-branch`) catches untested conditional paths

## Key Takeaways
- Use pytest with fixtures and parameterize
- Test behavior, not implementation; mock at external boundaries only
- Arrange-Act-Assert for test structure
- `breakpoint()` for debugging, `logging` over `print`
- repr (`!r`) for unambiguous debug output
- High coverage on critical paths, branch coverage for conditionals
