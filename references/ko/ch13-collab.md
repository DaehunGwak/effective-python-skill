# 13–14장: 협업 (항목 116–125)

## 의존성 찾기와 관리

### pip와 PyPI를 책임감 있게 사용
- 애플리케이션에서는 `requirements.txt`에 정확한 버전을 고정: `requests==2.31.0`
- 라이브러리에서는 `pyproject.toml`에 범위를 사용: `requests>=2.28,<3`
- 의존성 해석과 잠금 파일에는 `uv` 또는 `pip-tools` 사용
- 활발한 커뮤니티가 있는 잘 관리되는 패키지를 선호

### 가상 환경은 필수
```bash
# uv를 사용한 현대적 접근
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# 또는 고전적인 venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
절대 패키지를 전역으로 설치하지 마라. 모든 프로젝트가 자체 가상 환경을 갖는다.

## 문서화

### 모든 공개 함수, 클래스, 모듈에 독스트링 작성
```python
def calculate_distance(
    origin: tuple[float, float],
    destination: tuple[float, float],
) -> float:
    """두 GPS 좌표 사이의 대원 거리를 계산한다.

    하버사인 공식을 사용한다. 좌표는 (위도, 경도)를 도(degree) 단위로 나타낸다.

    Args:
        origin: 시작점 (위도, 경도).
        destination: 도착점 (위도, 경도).

    Returns:
        킬로미터 단위의 거리.

    Raises:
        ValueError: 좌표가 유효 범위를 벗어난 경우.
    """
```

### 독스트링 규칙
- 첫 줄: 한 문장 요약 (명령형: "계산한다", "~한다" 형태)
- 긴 독스트링에서는 요약 뒤에 빈 줄
- Args, Returns, Raises 섹션 (Google 스타일 또는 NumPy 스타일 — 하나를 정하고, 일관되게)
- 모듈 레벨 독스트링은 모듈의 목적을 기술
- 클래스 독스트링은 구현이 아닌 행위를 기술

## 패키지 구조

### 모듈 구성에 패키지 사용
```
myproject/
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py      # 공개 API
│       ├── core.py
│       ├── models.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
└── tests/
    ├── conftest.py
    └── test_core.py
```

### __init__.py에서 명시적 공개 API 정의
```python
# mypackage/__init__.py
from mypackage.core import process, transform
from mypackage.models import User, Config

__all__ = ["process", "transform", "User", "Config"]
```
이것은 `from mypackage import *`가 무엇을 내보내는지 제어하고,
의도된 공개 인터페이스를 문서화한다.

### 설정을 위한 모듈 스코프 코드
배포 환경별 동작을 설정하기 위해 모듈 레벨 코드를 사용하라:
```python
# config.py
import os

ENVIRONMENT = os.environ.get("APP_ENV", "development")

if ENVIRONMENT == "production":
    DATABASE_URL = os.environ["DATABASE_URL"]
    DEBUG = False
else:
    DATABASE_URL = "sqlite:///dev.db"
    DEBUG = True
```

## 라이브러리를 위한 에러 처리

### 라이브러리에 루트 예외 정의
```python
# mylib/exceptions.py
class MyLibError(Exception):
    """mylib의 기본 예외."""

class ConnectionError(MyLibError):
    """서비스 연결 실패."""

class AuthError(MyLibError):
    """인증 실패."""
```
호출자는 `except MyLibError`로 라이브러리의 모든 에러를 포착하면서도,
개별 에러 타입에 대한 구체적 처리도 가능하다.

### 순환 의존성 해결
순환 임포트는 설계 냄새(code smell)이다. 선호 순서대로의 해결책:
1. **구조 변경**: 공유 코드를 새 모듈로 이동
2. **사용 시점 임포트**: 임포트를 필요한 함수 내부로 이동
3. **`TYPE_CHECKING` 사용**: 타입 힌트에서만 임포트
```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypackage.models import User

def process(user: User) -> None:  # 타입 힌트는 동작하고, 순환 임포트 없음
    ...
```

## 정적 분석과 타입 체킹

### 런타임 전에 버그를 잡기 위한 타이핑
```python
# pyproject.toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
```

### 점진적 타이핑
한 번에 모든 것을 타입 지정하려고 하지 마라. 다음부터 시작하라:
1. 공개 API 함수
2. 복잡한 내부 함수
3. `mypy --strict`로 점진적으로 강화

### API 마이그레이션에는 `warnings` 사용
```python
import warnings

def old_function():
    warnings.warn(
        "old_function은 폐기 예정입니다, 대신 new_function을 사용하세요",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_function()
```

## 핵심 정리
- 모든 프로젝트에 가상 환경, 앱에는 고정된 의존성
- 모든 공개 API에 독스트링 (Google/NumPy 스타일, 하나를 정하라)
- 명시적 공개 인터페이스 정의에 `__init__.py` + `__all__`
- 라이브러리에는 루트 예외 클래스
- 순환 임포트는 구조 변경 또는 TYPE_CHECKING으로 해결
- mypy로 점진적 타이핑, 공개 API부터 시작
- 폐기와 마이그레이션 경로에는 `warnings`
