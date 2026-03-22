# Chapter 8: Metaclasses and Dynamic Attributes (Items 61–71)

## Dynamic Attributes

### Use __getattr__ for lazy attributes
`__getattr__` is called only when normal attribute lookup fails — use it for
lazy loading, proxy patterns, or schema-less data access:
```python
class LazyDB:
    def __getattr__(self, name: str):
        value = self._load_from_db(name)
        setattr(self, name, value)  # Cache for future access
        return value
```

### Use __getattribute__ with extreme caution
`__getattribute__` intercepts EVERY attribute access, including internal ones.
It's easy to create infinite recursion. Almost always, `__getattr__` is what you want.

### Use __setattr__ for attribute validation
```python
class ValidatedRecord:
    def __setattr__(self, name: str, value: object) -> None:
        if name == "age" and isinstance(value, int) and value < 0:
            raise ValueError("age must be non-negative")
        super().__setattr__(name, value)
```

## Metaclass Alternatives (Prefer These)

### __init_subclass__ for registration and validation
Before reaching for a metaclass, use `__init_subclass__` (3.6+):
```python
class Plugin:
    _registry: dict[str, type] = {}

    def __init_subclass__(cls, *, name: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        if name:
            Plugin._registry[name] = cls

class AuthPlugin(Plugin, name="auth"):
    ...

class CachePlugin(Plugin, name="cache"):
    ...

# Plugin._registry == {"auth": AuthPlugin, "cache": CachePlugin}
```
This covers 90% of the use cases that people historically reached for metaclasses for.

### Class decorators for class-level modification
```python
def add_repr(cls):
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Config:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
```
Class decorators are simpler, more explicit, and composable.

### __set_name__ for descriptor context
```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_{name}"
```
This gives descriptors access to their attribute name without metaclass magic.

## When Metaclasses ARE Appropriate

Use metaclasses only when you need to:
- Modify the class creation process itself (not just the result)
- Enforce structural constraints across entire class hierarchies
- Integrate with frameworks that require it (ORMs, serialization)

```python
class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        fields = {k: v for k, v in namespace.items() if isinstance(v, Field)}
        cls = super().__new__(mcs, name, bases, namespace)
        cls._fields = fields
        return cls
```

Prefer `__init_subclass__` + class decorators for 95% of cases.

## Annotations and __annotations__

- `__annotations__` stores type hints as a dict at the class level
- Use `typing.get_type_hints()` to resolve forward references properly
- Annotations are metadata — they don't enforce types at runtime

## Key Takeaways
- `__getattr__` for lazy/proxy attributes, avoid `__getattribute__`
- `__init_subclass__` replaces most metaclass use cases (registration, validation)
- Class decorators for post-creation class modification
- `__set_name__` for descriptor self-awareness
- Only use metaclasses when nothing else works
