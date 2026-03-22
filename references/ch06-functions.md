# Chapter 6: Functions (Items 30–44)

## Return Values

### Return dedicated result objects, not long tuples
When a function returns more than three values, callers lose track of positions.
Use a dataclass or NamedTuple:
```python
# Bad: Positional unpacking is fragile
def analyze(data):
    return mean, median, mode, stddev, count

m, md, mo, sd, n = analyze(data)  # Which is which?

# Good: Named fields
@dataclass
class Stats:
    mean: float
    median: float
    mode: float
    stddev: float
    count: int

def analyze(data) -> Stats:
    ...
    return Stats(mean=m, median=md, mode=mo, stddev=sd, count=n)
```

### Raise exceptions instead of returning None
Returning `None` for "not found" or "error" is ambiguous — `None`, `0`, and `""` are
all falsy. Raise a specific exception to make failure impossible to ignore:
```python
# Bad: None is ambiguous
def find_user(id: int) -> User | None:
    ...

# Good: Explicit failure mode
class UserNotFoundError(Exception):
    pass

def find_user(id: int) -> User:
    user = db.get(id)
    if user is None:
        raise UserNotFoundError(f"No user with id={id}")
    return user
```

## Closures and Scope

### nonlocal for mutable closure state
If a closure needs to modify a variable from the enclosing scope, use `nonlocal`:
```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```
But prefer a class if the state grows beyond one or two variables — closures with
lots of `nonlocal` declarations are hard to follow.

## Arguments

### Variable positional arguments (*args)
Use `*args` to reduce visual noise when a function accepts any number of similar items:
```python
def log(message: str, *values: object) -> None:
    if values:
        print(f"{message}: {', '.join(str(v) for v in values)}")
    else:
        print(message)
```
Caveat: `*args` consumes an entire generator into a tuple — avoid with large iterables.

### Keyword-only arguments
Force clarity at call sites by making arguments keyword-only (after `*`):
```python
# Good: Can't accidentally swap timeout and retries
def fetch(url: str, *, timeout: float = 30, retries: int = 3) -> Response:
    ...

fetch("https://api.example.com", timeout=10, retries=5)
```

### Positional-only arguments (/)
Use `/` to prevent callers from using parameter names that might change:
```python
def distance(x1: float, y1: float, x2: float, y2: float, /) -> float:
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
```

### Never use mutable default arguments
```python
# WRONG: Shared mutable default
def append_to(item, target=[]):  # Bug! Same list every call
    target.append(item)
    return target

# Correct: Use None sentinel
def append_to(item, target: list | None = None) -> list:
    if target is None:
        target = []
    target.append(item)
    return target
```

## Decorators

### Use functools.wraps always
```python
from functools import wraps

def retry(max_attempts: int = 3):
    def decorator(func):
        @wraps(func)  # Preserves __name__, __doc__, etc.
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
        return wrapper
    return decorator
```

### Decorator ordering matters
Decorators apply bottom-up. Put `@functools.wraps` innermost,
observability decorators (logging, tracing) outermost.

## Type Hints for Functions

### Annotate return types, especially None
```python
def process(data: list[int]) -> None:  # Explicit None return
    ...

def compute(x: float) -> float:  # Return type documents contract
    return x ** 2
```

### Use `Callable` for function parameters
```python
from collections.abc import Callable

def apply_transform(
    data: list[int],
    transform: Callable[[int], int],
) -> list[int]:
    return [transform(x) for x in data]
```

## Key Takeaways
- Return dataclasses/NamedTuples instead of long tuples
- Raise exceptions instead of returning None for errors
- Keyword-only args (`*`) for all non-obvious parameters
- Never use mutable defaults — use `None` sentinel pattern
- Always `@wraps` your decorators
- Type-annotate all function signatures
