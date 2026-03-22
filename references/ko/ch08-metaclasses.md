# 8장: 메타클래스와 동적 속성 (항목 61–71)

## 동적 속성

### 지연 속성에는 __getattr__ 사용
`__getattr__`는 일반적인 속성 조회가 실패할 때만 호출된다 —
지연 로딩, 프록시 패턴, 스키마 없는 데이터 접근에 사용하라:
```python
class LazyDB:
    def __getattr__(self, name: str):
        value = self._load_from_db(name)
        setattr(self, name, value)  # 이후 접근을 위해 캐시
        return value
```

### __getattribute__는 극도의 주의로 사용
`__getattribute__`는 내부 속성을 포함하여 모든 속성 접근을 가로챈다.
무한 재귀를 만들기 쉽다. 거의 항상 `__getattr__`가 원하는 것이다.

### 속성 유효성 검증에는 __setattr__
```python
class ValidatedRecord:
    def __setattr__(self, name: str, value: object) -> None:
        if name == "age" and isinstance(value, int) and value < 0:
            raise ValueError("age는 음수가 될 수 없습니다")
        super().__setattr__(name, value)
```

## 메타클래스 대안 (이것들을 선호하라)

### 등록과 유효성 검증에는 __init_subclass__
메타클래스에 손을 뻗기 전에, `__init_subclass__` (3.6+)를 사용하라:
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
이것은 역사적으로 메타클래스를 사용했던 유스케이스의 90%를 커버한다.

### 클래스 레벨 수정에는 클래스 데코레이터
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
클래스 데코레이터는 더 단순하고, 더 명시적이며, 조합 가능하다.

### 디스크립터 컨텍스트에는 __set_name__
```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_{name}"
```
이것은 메타클래스 마법 없이 디스크립터가 자신의 속성 이름에 접근할 수 있게 한다.

## 메타클래스가 적절한 경우

메타클래스는 다음이 필요할 때만 사용하라:
- 클래스 생성 과정 자체를 수정해야 할 때 (결과뿐 아니라)
- 전체 클래스 계층에 걸쳐 구조적 제약을 강제해야 할 때
- 메타클래스가 필요한 프레임워크와 통합할 때 (ORM, 직렬화)

```python
class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        fields = {k: v for k, v in namespace.items() if isinstance(v, Field)}
        cls = super().__new__(mcs, name, bases, namespace)
        cls._fields = fields
        return cls
```

95%의 경우에는 `__init_subclass__` + 클래스 데코레이터를 선호하라.

## 어노테이션과 __annotations__

- `__annotations__`는 클래스 레벨에서 타입 힌트를 딕셔너리로 저장
- 전방 참조를 올바르게 해석하려면 `typing.get_type_hints()`를 사용
- 어노테이션은 메타데이터이다 — 런타임에 타입을 강제하지 않는다

## 핵심 정리
- 지연/프록시 속성에는 `__getattr__`, `__getattribute__`는 피하라
- 대부분의 메타클래스 유스케이스를 `__init_subclass__`가 대체 (등록, 유효성 검증)
- 생성 후 클래스 수정에는 클래스 데코레이터
- 디스크립터 자기 인식에는 `__set_name__`
- 다른 것으로 안 될 때만 메타클래스 사용
