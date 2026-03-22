# 🐍 Effective Python — Claude Code 스킬

> [Effective Python 3판](https://effectivepython.com/) (Brett Slatkin, 125개 항목)의 원칙을 [Claude Code](https://code.claude.com/)로 Python 코드를 작성, 리뷰, 리팩토링할 때 자동으로 적용합니다.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Skill](https://img.shields.io/badge/claude--code-skill-blueviolet.svg)](https://code.claude.com/docs/en/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 왜 이 스킬이 필요한가?

Claude Code는 이미 괜찮은 Python을 작성합니다 — 하지만 "괜찮은" 코드는 "파이썬다운(Pythonic)" 코드가 아닙니다. 이 스킬은 Brett Slatkin의 Effective Python에서 검증된 **125가지 원칙**을 인코딩하여, Claude Code가 일관되게 관용적이고, 유지보수하기 쉽고, 고성능인 코드를 생성하도록 합니다.

**이 스킬 없이** Claude는 다음과 같이 작성할 수 있습니다:
- `enumerate` 대신 `range(len(items))` 사용
- 예외를 발생시키는 대신 에러 시 `None` 반환
- 가변 기본 인자 사용
- 컴포지션 대신 깊은 상속 계층 구축

**이 스킬이 적용되면**, Claude Code는 기본적으로 Effective Python 원칙을 따릅니다.

## 빠른 설치

```bash
# 한 줄 설치 (프로젝트 레벨)
git clone https://github.com/YOUR_USERNAME/effective-python-skill.git .claude/skills/effective-python

# 또는 전역 설치 (모든 프로젝트에 적용)
git clone https://github.com/YOUR_USERNAME/effective-python-skill.git ~/.claude/skills/effective-python
```

또는 설치 스크립트를 사용할 수 있습니다:

```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/effective-python-skill/main/install.sh | bash
```

## 사용법

### 자동 모드 — Python만 작성하세요

설치 후, Claude Code가 Python을 생성할 때 스킬이 자동으로 활성화됩니다.
별도의 명령이 필요 없습니다 — Claude에게 코드를 작성해달라고 하면 Effective Python 원칙이 자동 적용됩니다.

### 리뷰 모드 — 기존 코드 감사

```
/effective-python src/mypackage/
```

Effective Python 체크리스트에 대한 종합적인 리뷰를 수행합니다:

```
🔴 심각 — src/api/handler.py:42
   가변 기본 인자: def process(items, cache={})
   → None 센티널 사용: def process(items, cache=None)

🟡 제안 — src/models/user.py:15
   에러 시 None을 반환하고 있음. 대신 UserNotFoundError를 발생시키세요.
   → 호출자가 "찾지 못함"과 falsy 값을 혼동할 수 없게 됩니다.

🟢 우수 — src/utils/transform.py:8
   제너레이터 표현식과 itertools.chain의 깔끔한 사용
```

### 리팩토링 모드 — 코드 현대화

```
/effective-python refactor src/legacy_module.py
```

어떤 Effective Python 원칙이 적용되었는지와 함께 변경 전/후를 보여줍니다.

### 정적 분석 스크립트

일반적인 안티패턴에 대한 빠른 AST 기반 스캔:

```bash
python .claude/skills/effective-python/scripts/check_patterns.py src/
```

감지 항목: 가변 기본값, bare except, `range(len())`, 반복문 내 문자열 연결,
타입 어노테이션 누락, `isinstance` 체이닝 등.

## 아키텍처

```
effective-python/
├── SKILL.md                    # 오케스트레이터 + 라우팅 테이블 (126줄)
├── references/                 # 챕터별 가이드라인 (지연 로딩)
│   ├── ch01-pythonic.md       # 파이썬다운 사고 — 문법, 표현식, 스타일
│   ├── ch02-strings.md       # 문자열, 바이트, 슬라이싱
│   ├── ch03-loops.md         # 반복문, 이터레이터, enumerate, zip, itertools
│   ├── ch04-dicts.md         # 딕셔너리, defaultdict, __missing__
│   ├── ch05-generators.md    # 컴프리헨션, 제너레이터, yield
│   ├── ch06-functions.md     # 함수 시그니처, 데코레이터, 클로저
│   ├── ch07-classes.md       # 데이터클래스, 컴포지션, 인터페이스
│   ├── ch08-metaclasses.md   # __init_subclass__, 디스크립터
│   ├── ch09-concurrency.md   # 스레딩, asyncio, 병렬 처리
│   ├── ch10-robustness.md    # 에러 처리, 방어적 코딩 (3판 신규)
│   ├── ch11-performance.md   # 프로파일링, 최적화 (3판 신규)
│   ├── ch12-testing.md       # pytest, 디버깅, 커버리지
│   └── ch13-collab.md       # 패키징, 독스트링, 타입 힌트
├── scripts/
│   └── check_patterns.py      # AST 기반 안티패턴 감지기
├── install.sh                  # 원커맨드 설치 스크립트
├── LICENSE
└── README.md
```

### 점진적 공개 패턴

이 스킬은 컨텍스트 윈도우를 초과하지 않으면서 125개 항목을 처리합니다:

| 레이어 | 크기 | 로딩 시점 |
|--------|------|-----------|
| 메타데이터 (이름 + 설명) | ~100 토큰 | 항상 컨텍스트에 포함 |
| SKILL.md 본문 (라우팅 + 범용 규칙) | 126줄 | 스킬 트리거 시 |
| 레퍼런스 파일 (챕터별) | 67~172줄 각각 | 관련 챕터만 |
| 스크립트 (check_patterns.py) | 157줄 | 명시적 호출 시에만 |

코드 생성 시에는 1~2개의 레퍼런스 파일만 로드됩니다. 전체 리뷰 시에는 관련 챕터가 필요에 따라 로드됩니다. 이를 통해 125개 원칙을 모두 다루면서도 토큰 사용을 효율적으로 유지합니다.

## 다루는 내용

| 챕터 | 항목 | 핵심 원칙 |
|------|------|-----------|
| 파이썬다운 사고 | 1–16 | f-string, 언패킹, 왈러스 연산자, match/case |
| 문자열과 슬라이싱 | 10–16 | 스트라이드 제한, `removeprefix`, bytes/str 경계 |
| 반복문과 이터레이터 | 17–24 | `enumerate`, `zip(strict=True)`, `itertools`, `any`/`all` |
| 딕셔너리 | 25–29 | `get()`, `defaultdict`, `__missing__`, 중첩 제한 |
| 컴프리헨션 | 30–36 | 최대 2개 `for` 절, 리스트보다 제너레이터, `yield from` |
| 함수 | 30–44 | 키워드 전용 인자, `None` 센티널, `@wraps`, 결과 객체 |
| 클래스 | 45–60 | 상속보다 컴포지션, `Protocol`, `@dataclass(slots=True)` |
| 메타클래스 | 61–71 | 메타클래스 대신 `__init_subclass__`, 디스크립터 |
| 동시성 | 72–82 | GIL 인식, `TaskGroup`, `asyncio.to_thread`, `Lock` |
| 견고성 | 83–92 | 좁은 `try` 블록, 예외 계층, 경계 검증 |
| 성능 | 93–103 | 프로파일링 우선, 자료구조 선택, 최적화 사다리 |
| 테스팅 | 104–115 | pytest 픽스처, 행위 테스팅, `breakpoint()`, 로깅 |
| 협업 | 116–125 | 독스트링, `__all__`, 가상 환경, 점진적 타이핑 |

## 커스터마이징

### 프로젝트별 규칙 추가

새 레퍼런스 파일을 만들고 SKILL.md의 라우팅 테이블에 등록합니다:

```markdown
# references/ch-myproject.md 에서
# 프로젝트별 패턴 작성...

# SKILL.md 라우팅 테이블에 추가:
| Django 뷰/모델 | `references/ch-django.md` |
```

### 심각도 조정

SKILL.md의 범용 원칙 섹션을 편집하여 팀에서 가장 중요하게 생각하는 사항을 강조합니다.

## 저작권 안내

이 스킬은 책에서 **영감을 받은 원칙과 패턴**을 독자적인 표현으로 인코딩합니다.
책의 원문을 재현하지 않습니다. 전체 설명, 맥락, 예제를 위해
[Effective Python 구매](https://effectivepython.com/)를 강력히 권장합니다.

## 기여하기

1. 이 저장소를 포크합니다
2. 레퍼런스 파일을 추가하거나 개선합니다
3. 샘플 코드에 대해 `python scripts/check_patterns.py`로 테스트합니다
4. 어떤 원칙을 추가/개선했는지 설명과 함께 PR을 제출합니다

## 라이선스

MIT — 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.
