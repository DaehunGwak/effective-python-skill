# 12장: 테스팅과 디버깅 (항목 104–115)

## 테스팅 철학

### 모든 함수와 클래스에 테스트 작성
테스트는 항상 최신 상태인 문서이다. 코드가 무엇을 해야 하는지 기술하고
회귀를 잡아낸다. 테스트되지 않았다면, 동작하지 않는 것이다.

### unittest 말고 pytest 사용
pytest는 현대 파이썬의 표준이다. 장점:
- `self.assertEqual` 대신 일반 `assert` — 더 읽기 쉽고, 더 나은 에러 메시지
- setUp/tearDown 대신 픽스처 — 조합 가능, 재사용 가능, 명시적
- 여러 입력을 간결하게 테스트하는 파라미터화
- 풍부한 플러그인 에코시스템 (pytest-cov, pytest-mock, pytest-asyncio)

```python
# 좋음: pytest 스타일
def test_parse_valid_input():
    result = parse("42")
    assert result == 42

def test_parse_invalid_input():
    with pytest.raises(ValueError, match="invalid"):
        parse("not_a_number")
```

### 테스트 의존성에는 픽스처 사용
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

### 반복을 피하기 위한 파라미터화
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

## 테스트 설계

### 구현이 아닌 행위를 테스트
테스트는 코드가 무엇을 하는지를 기술해야 하지, 어떻게 하는지를 기술해서는 안 된다:
```python
# 나쁨: 구현 세부사항을 테스트
def test_cache_uses_dict():
    cache = Cache()
    assert isinstance(cache._store, dict)

# 좋음: 행위를 테스트
def test_cache_returns_stored_value():
    cache = Cache()
    cache.set("key", "value")
    assert cache.get("key") == "value"
```

### 모킹은 절제하고 전략적으로 사용
외부 경계(HTTP 호출, 데이터베이스, 파일 시스템)를 모킹하라, 내부 코드가 아니라:
```python
# 좋음: 외부 경계를 모킹
def test_fetch_user(mocker):
    mocker.patch("myapp.http.get", return_value={"name": "Alice"})
    user = fetch_user(42)
    assert user.name == "Alice"

# 나쁨: 내부 구현을 모킹
def test_process(mocker):
    mocker.patch("myapp.internal._helper", return_value=42)  # 너무 결합됨
```

### Arrange-Act-Assert 패턴
```python
def test_transfer():
    # Arrange (준비)
    source = Account(balance=100)
    target = Account(balance=50)

    # Act (실행)
    transfer(source, target, amount=30)

    # Assert (검증)
    assert source.balance == 70
    assert target.balance == 80
```

## 디버깅

### 대화형 디버깅에는 breakpoint() 사용
```python
def complex_function(data):
    intermediate = transform(data)
    breakpoint()  # pdb (또는 설정된 디버거)로 진입
    return finalize(intermediate)
```
프로덕션에서 모든 브레이크포인트를 비활성화하려면 `PYTHONBREAKPOINT=0`을 설정하라.

### 모호하지 않은 디버그 출력에는 repr() 사용
```python
# 모호함
print(f"value: {x}")      # "value: None" — 문자열 "None"인가 NoneType인가?

# 모호하지 않음
print(f"value: {x!r}")    # "value: None" vs "value: 'None'"
```

### print 대신 logging 사용
```python
import logging

logger = logging.getLogger(__name__)

logger.debug("항목 %s 처리 중", item_id)
logger.info("배치 완료: %d개 항목", count)
logger.warning("%s에 대한 재시도 %d/%d", url, attempt, max_attempts)
logger.error("처리 실패: %s", error, exc_info=True)
```
로깅은 애플리케이션 진입점에서 설정하라, 라이브러리 코드에서가 아니라.

## 테스트 커버리지

### 핵심 경로에서 높은 커버리지를 목표로
- 100% 커버리지가 버그가 없음을 의미하지는 않는다 — 하지만 0% 커버리지는 버그를 보장한다
- 보일러플레이트가 아닌 비즈니스 로직에 커버리지를 집중하라
- 측정에 `pytest-cov` 사용: `pytest --cov=myapp --cov-report=term-missing`
- 브랜치 커버리지(`--cov-branch`)가 테스트되지 않은 조건부 경로를 잡아낸다

## 핵심 정리
- 픽스처와 파라미터화와 함께 pytest 사용
- 구현이 아닌 행위를 테스트; 외부 경계에서만 모킹
- 테스트 구조에는 Arrange-Act-Assert
- 디버깅에는 `breakpoint()`, `print` 대신 `logging`
- 모호하지 않은 디버그 출력에 repr (`!r`)
- 핵심 경로에서 높은 커버리지, 조건문에는 브랜치 커버리지
