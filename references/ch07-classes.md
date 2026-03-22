# Chapter 7: Classes and Interfaces (Items 45–60)

## Composition Over Inheritance

### Prefer composition and delegation
Deep inheritance hierarchies are fragile. Compose behavior by holding references:
```python
# Bad: Fragile inheritance chain
class LoggingList(list):
    def append(self, item):
        log(f"Adding {item}")
        super().append(item)
    # But insert(), extend(), __iadd__ are NOT logged!

# Good: Composition with clear delegation
class TrackedCollection:
    def __init__(self) -> None:
        self._items: list = []
        self._log: list[str] = []

    def add(self, item: object) -> None:
        self._log.append(f"Added {item}")
        self._items.append(item)
```

### Use mix-ins for shared behavior
Mix-ins provide reusable functionality without creating "is-a" relationships:
```python
class JsonMixin:
    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, data: str):
        return cls(**json.loads(data))

@dataclass
class Config(JsonMixin):
    host: str
    port: int
```
Rules for mix-ins: no `__init__`, no instance state, single narrow responsibility.

## Dataclasses and NamedTuple

### Use @dataclass for structured data
```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

@dataclass(frozen=True)  # Immutable — usable as dict keys
class Color:
    r: int
    g: int
    b: int

@dataclass
class Config:
    name: str
    tags: list[str] = field(default_factory=list)  # Mutable default done right
```

### NamedTuple for lightweight immutable records
```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    label: str = ""
```
NamedTuples are tuples — they support indexing and iteration. Use when you need
tuple compatibility (e.g., as dict keys, in sets). Use `@dataclass(frozen=True)`
when you want more control (custom methods, slots, etc.).

## Properties and Descriptors

### Use @property for computed attributes
```python
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius must be non-negative")
        self._radius = value

    @property
    def area(self) -> float:
        return math.pi * self._radius ** 2
```

### Prefer descriptors over repeated @property
When multiple attributes share the same validation logic, use a descriptor:
```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name, None)

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name[1:]} must be positive")
        setattr(obj, self.name, value)

class Shape:
    width = Positive()
    height = Positive()
```

## Interface Patterns

### Protocol for structural typing
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self, canvas: Canvas) -> None: ...

def render(item: Drawable, canvas: Canvas) -> None:
    item.draw(canvas)  # Any object with a draw() method works
```
`Protocol` is Python's answer to Go-style interfaces — no inheritance required.

### Abstract base classes for enforcement
Use `abc.ABC` when you need to enforce that subclasses implement specific methods:
```python
from abc import ABC, abstractmethod

class Serializer(ABC):
    @abstractmethod
    def serialize(self, data: object) -> bytes: ...

    @abstractmethod
    def deserialize(self, raw: bytes) -> object: ...
```

## Slots for Memory Efficiency
```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
```
`__slots__` prevents `__dict__` creation, reducing memory 40-50% for many instances.
Use when creating millions of small objects.

## Key Takeaways
- Composition over inheritance; mix-ins for shared behavior
- `@dataclass` for structured data, `frozen=True` for immutable
- `Protocol` for duck-typing interfaces, `ABC` for enforcement
- Descriptors when property validation logic repeats across attributes
- `__slots__` (or `@dataclass(slots=True)`) for memory-sensitive hot paths
