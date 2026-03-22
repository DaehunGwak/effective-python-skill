# 7장: 클래스와 인터페이스 (항목 45–60)

## 상속보다 컴포지션

### 컴포지션과 위임 선호
깊은 상속 계층은 취약하다. 참조를 보유하여 행위를 구성하라:
```python
# 나쁨: 취약한 상속 체인
class LoggingList(list):
    def append(self, item):
        log(f"추가: {item}")
        super().append(item)
    # 하지만 insert(), extend(), __iadd__는 로깅되지 않는다!

# 좋음: 명확한 위임을 가진 컴포지션
class TrackedCollection:
    def __init__(self) -> None:
        self._items: list = []
        self._log: list[str] = []

    def add(self, item: object) -> None:
        self._log.append(f"추가됨: {item}")
        self._items.append(item)
```

### 공유 행위에는 믹스인 사용
믹스인은 "is-a" 관계를 만들지 않으면서 재사용 가능한 기능을 제공한다:
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
믹스인 규칙: `__init__` 없음, 인스턴스 상태 없음, 단일 좁은 책임.

## 데이터클래스와 NamedTuple

### 구조화된 데이터에는 @dataclass 사용
```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

@dataclass(frozen=True)  # 불변 — dict 키로 사용 가능
class Color:
    r: int
    g: int
    b: int

@dataclass
class Config:
    name: str
    tags: list[str] = field(default_factory=list)  # 가변 기본값을 올바르게 처리
```

### 경량 불변 레코드에는 NamedTuple
```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    label: str = ""
```
NamedTuple은 튜플이다 — 인덱싱과 순회를 지원한다. 튜플 호환성이
필요할 때(예: dict 키, 셋 내부) 사용하라. 더 많은 제어(커스텀 메서드, slots 등)가
필요하면 `@dataclass(frozen=True)`를 사용하라.

## 프로퍼티와 디스크립터

### 계산된 속성에는 @property 사용
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
            raise ValueError("반지름은 음수가 될 수 없습니다")
        self._radius = value

    @property
    def area(self) -> float:
        return math.pi * self._radius ** 2
```

### 반복되는 @property보다 디스크립터 선호
여러 속성이 같은 유효성 검증 로직을 공유한다면, 디스크립터를 사용하라:
```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name, None)

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name[1:]}은(는) 양수여야 합니다")
        setattr(obj, self.name, value)

class Shape:
    width = Positive()
    height = Positive()
```

## 인터페이스 패턴

### 구조적 타이핑에는 Protocol
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self, canvas: Canvas) -> None: ...

def render(item: Drawable, canvas: Canvas) -> None:
    item.draw(canvas)  # draw() 메서드가 있는 모든 객체가 동작
```
`Protocol`은 Go 스타일 인터페이스에 대한 파이썬의 답이다 — 상속이 필요 없다.

### 강제를 위한 추상 기본 클래스
서브클래스가 특정 메서드를 구현하도록 강제해야 할 때 `abc.ABC`를 사용하라:
```python
from abc import ABC, abstractmethod

class Serializer(ABC):
    @abstractmethod
    def serialize(self, data: object) -> bytes: ...

    @abstractmethod
    def deserialize(self, raw: bytes) -> object: ...
```

## 메모리 효율을 위한 Slots
```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
```
`__slots__`는 `__dict__` 생성을 방지하여, 많은 인스턴스에서 메모리를 40-50% 절감한다.
수백만 개의 작은 객체를 만들 때 사용하라.

## 핵심 정리
- 상속보다 컴포지션; 공유 행위에는 믹스인
- 구조화된 데이터에는 `@dataclass`, 불변에는 `frozen=True`
- 덕 타이핑 인터페이스에는 `Protocol`, 강제에는 `ABC`
- 속성 유효성 검증 로직이 반복될 때 디스크립터
- 메모리 민감한 핫 패스에는 `__slots__` (또는 `@dataclass(slots=True)`)
