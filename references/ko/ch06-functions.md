# 6장: 함수 (항목 30–44)

## 반환값

### 긴 튜플 대신 전용 결과 객체 반환
함수가 세 개 이상의 값을 반환할 때, 호출자는 위치를 추적하지 못한다.
데이터클래스나 NamedTuple을 사용하라:
```python
# 나쁨: 위치 기반 언패킹은 깨지기 쉬움
def analyze(data):
    return mean, median, mode, stddev, count

m, md, mo, sd, n = analyze(data)  # 어떤 게 어떤 것인지?

# 좋음: 이름이 있는 필드
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

### None을 반환하는 대신 예외 발생
"찾지 못함"이나 "에러"에 대해 `None`을 반환하는 것은 모호하다 — `None`, `0`, `""`는
모두 falsy이다. 실패를 무시할 수 없게 특정 예외를 발생시키라:
```python
# 나쁨: None은 모호함
def find_user(id: int) -> User | None:
    ...

# 좋음: 명시적 실패 모드
class UserNotFoundError(Exception):
    pass

def find_user(id: int) -> User:
    user = db.get(id)
    if user is None:
        raise UserNotFoundError(f"id={id}인 사용자 없음")
    return user
```

## 클로저와 스코프

### 가변 클로저 상태에는 nonlocal
클로저가 둘러싼 스코프의 변수를 수정해야 할 때, `nonlocal`을 사용하라:
```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```
하지만 상태가 한두 개 변수를 넘어서면 클래스를 선호하라 — `nonlocal` 선언이
많은 클로저는 추적하기 어렵다.

## 인자

### 가변 위치 인자 (*args)
함수가 비슷한 항목을 여러 개 받을 때 `*args`를 사용하여 시각적 노이즈를 줄이라:
```python
def log(message: str, *values: object) -> None:
    if values:
        print(f"{message}: {', '.join(str(v) for v in values)}")
    else:
        print(message)
```
주의: `*args`는 제너레이터 전체를 튜플로 소비한다 — 대용량 이터러블에서는 피하라.

### 키워드 전용 인자
`*` 뒤에 위치시켜 호출 지점에서 명확성을 강제하라:
```python
# 좋음: timeout과 retries를 실수로 바꿀 수 없음
def fetch(url: str, *, timeout: float = 30, retries: int = 3) -> Response:
    ...

fetch("https://api.example.com", timeout=10, retries=5)
```

### 위치 전용 인자 (/)
변경될 수 있는 매개변수 이름을 호출자가 사용하지 못하게 `/`를 사용하라:
```python
def distance(x1: float, y1: float, x2: float, y2: float, /) -> float:
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
```

### 가변 기본 인자를 절대 사용하지 마라
```python
# 잘못됨: 공유되는 가변 기본값
def append_to(item, target=[]):  # 버그! 매 호출마다 같은 리스트
    target.append(item)
    return target

# 올바름: None 센티널 사용
def append_to(item, target: list | None = None) -> list:
    if target is None:
        target = []
    target.append(item)
    return target
```

## 데코레이터

### functools.wraps는 항상 사용
```python
from functools import wraps

def retry(max_attempts: int = 3):
    def decorator(func):
        @wraps(func)  # __name__, __doc__ 등을 보존
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

### 데코레이터 순서가 중요하다
데코레이터는 아래에서 위로 적용된다. `@functools.wraps`는 가장 안쪽에,
관찰성 데코레이터(로깅, 트레이싱)는 가장 바깥쪽에 놓으라.

## 함수의 타입 힌트

### 반환 타입 어노테이션, 특히 None
```python
def process(data: list[int]) -> None:  # 명시적 None 반환
    ...

def compute(x: float) -> float:  # 반환 타입이 계약을 문서화
    return x ** 2
```

### 함수 파라미터에는 `Callable` 사용
```python
from collections.abc import Callable

def apply_transform(
    data: list[int],
    transform: Callable[[int], int],
) -> list[int]:
    return [transform(x) for x in data]
```

## 핵심 정리
- 긴 튜플 대신 데이터클래스/NamedTuple 반환
- 에러 시 None 반환 대신 예외 발생
- 비명시적 파라미터에는 키워드 전용 인자(`*`) 사용
- 가변 기본값 절대 사용 금지 — `None` 센티널 패턴 사용
- 데코레이터에는 항상 `@wraps`
- 모든 함수 시그니처에 타입 어노테이션
