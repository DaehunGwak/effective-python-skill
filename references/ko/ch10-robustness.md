# 10장: 견고성 (항목 83–92)

3판에서 새로 추가된 장으로, 깨지지 않는 코드 작성에 초점을 맞춘다.

## 예외 처리

### 구체적 예외 포착, 절대 bare except 금지
```python
# 나쁨: KeyboardInterrupt, SystemExit, 모든 것을 포착
try:
    process(data)
except:
    pass

# 나쁨: 여전히 범위가 너무 넓음
try:
    process(data)
except Exception:
    log("뭔가 잘못되었음")

# 좋음: 처리할 수 있는 것을 포착
try:
    result = parse(raw_input)
except (ValueError, json.JSONDecodeError) as e:
    return default_result(error=str(e))
```

### try 블록 범위 최소화
예외를 발생시킬 수 있는 특정 연산만 감싸라, 함수 본문 전체가 아니라:
```python
# 나쁨: 어떤 줄이 예외를 발생시켰는지?
try:
    data = load_file(path)
    parsed = parse(data)
    result = transform(parsed)
    save(result)
except FileNotFoundError:
    ...

# 좋음: 좁은 범위
try:
    data = load_file(path)
except FileNotFoundError:
    return None

parsed = parse(data)
result = transform(parsed)
save(result)
```

### try/except/else/finally를 올바르게 사용
```python
try:
    f = open(path)
except FileNotFoundError:
    handle_missing()
else:
    # 예외가 없을 때만 실행 — 성공 로직을 여기에
    data = f.read()
finally:
    # 항상 실행 — 정리 작업
    ...
```
`else` 절은 성공 경로에서 발생한 예외를 실수로 포착하는 것을 방지한다.

### 라이브러리에는 예외 계층 정의
```python
class MyLibraryError(Exception):
    """mylib의 루트 예외."""

class ConfigError(MyLibraryError):
    """설정이 유효하지 않음."""

class NetworkError(MyLibraryError):
    """네트워크 작업 실패."""
```
호출자는 넓은 처리를 위해 `MyLibraryError`를 포착하거나,
대상 복구를 위해 특정 서브클래스를 포착할 수 있다.

## 방어적 패턴

### 경계에서 검증, 내부에서는 신뢰
```python
# 공개 API 경계 — 검증
def create_user(name: str, age: int) -> User:
    if not name.strip():
        raise ValueError("name은 비어있으면 안 됩니다")
    if age < 0 or age > 150:
        raise ValueError(f"유효하지 않은 age: {age}")
    return _build_user(name.strip(), age)

# 내부 함수 — 데이터를 신뢰
def _build_user(name: str, age: int) -> User:
    return User(name=name, age=age)  # 여기서는 검증 없음
```

### 개발 불변 조건에는 assert 사용
```python
def process_batch(items: list[Item]) -> None:
    assert len(items) > 0, "빈 배치는 상위에서 필터링되었어야 함"
    assert all(item.is_valid for item in items), "배치에 유효하지 않은 항목 존재"
    ...
```
`assert` 문은 Python이 `-O` (최적화 플래그)로 실행될 때 제거된다.
프로덕션 코드에서 입력 검증에 절대 사용하지 마라.

### 보장된 정리를 위한 컨텍스트 매니저
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

### 폐기와 마이그레이션을 위한 warnings
```python
import warnings

def old_api(x):
    warnings.warn(
        "old_api()는 폐기 예정입니다, 대신 new_api()를 사용하세요",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_api(x)
```

## 우아한 성능 저하

### 폴백 체인 사용
```python
def get_config(key: str) -> str:
    # 우선순위대로 소스 시도
    if (val := os.environ.get(key)):
        return val
    if (val := config_file.get(key)):
        return val
    if (val := DEFAULTS.get(key)):
        return val
    raise ConfigError(f"{key}에 대한 값 없음")
```

### 지수 백오프로 재시도
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

## 핵심 정리
- 좁은 try 블록으로 구체적 예외 포착
- 성공 경로와 예외 처리를 분리하기 위해 `else` 절 사용
- 호출자를 절연하기 위해 라이브러리 루트 예외 정의
- 공개 API 경계에서 검증, 내부 불변 조건에는 assert 사용
- 리소스 정리에는 `contextmanager`, 마이그레이션에는 `warnings`
- 견고한 시스템을 위해 폴백 체인과 재시도 로직 구축
