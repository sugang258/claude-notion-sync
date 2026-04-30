# Claude → Notion 연동 시스템

Claude Code 대화를 `/save` 명령어 한 번으로 Notion 페이지에 자동 정리하는 시스템입니다.

## 개요

| 항목 | 내용 |
|------|------|
| 트리거 | `/save` 또는 `/reset-save` 명령어 입력 시 |
| 저장 범위 | 마지막 저장 이후 ~ 현재 대화 (첫 저장 시 전체) |
| 저장 형식 | 제목 / 날짜·시간 / 한줄 요약 / 다룬 주제 / 정리 / 결론 / 다음 단계 |
| 기술 스택 | Python + Notion API |

## 파일 구조

```
claude-notion-sync/
├── main.py                # 실행 진입점 (JSON stdin → Notion 저장, 에러 처리)
├── notion_writer.py       # Notion API 블록 생성 및 페이지 작성
├── requirements.txt       # 의존 패키지
├── .env                   # API 키 (직접 생성 필요, git 제외)
├── .env.example           # 환경 변수 형식 안내
└── last_save_marker.txt   # 마지막 저장 시점 기록 (자동 생성, git 제외)

~/.claude/commands/
├── save.md                # /save 슬래시 커맨드 정의 (전역)
└── reset-save.md          # /reset-save 슬래시 커맨드 정의 (전역)
```

## 동작 흐름

```
사용자가 /save 입력
    ↓
last_save_marker.txt 확인
    ├─ 있으면 → 마지막 저장 이후 대화만 분석
    └─ 없으면 → 전체 대화 분석 (첫 저장)
    ↓
Claude가 대화 분석 → JSON 생성
    ↓
python main.py << 'ENDJSON' ... ENDJSON
    ↓
notion_writer.py → Notion API 호출 (블록 100개 초과 시 분할 전송)
    ↓
Notion 부모 페이지 아래 새 자식 페이지 생성
    ↓
last_save_marker.txt 업데이트 → URL 출력
```

## 설치 방법

### 1. 레포지토리 클론

```bash
git clone https://github.com/sugang258/claude-notion-sync.git
cd claude-notion-sync
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. Notion Integration 생성

1. [Notion My Integrations](https://www.notion.so/my-integrations) 접속
2. **New integration** 클릭 → 이름 입력 후 Submit
3. **Internal Integration Token** 복사 (`secret_xxx...` 형태)

### 4. Notion 페이지 연동

1. 저장할 Notion 페이지 열기
2. 우측 상단 `...` → **Connect to** → 생성한 Integration 선택
3. 페이지 URL에서 ID 복사
   ```
   https://www.notion.so/페이지제목-{PAGE_ID}
                                      ↑ 이 부분
   ```

### 5. 환경 변수 설정

`.env.example`을 복사하여 `.env` 파일 생성 후 값 입력:

```
NOTION_API_KEY=secret_xxx...
NOTION_PAGE_ID=your_page_id_here
```

### 6. 슬래시 커맨드 등록

#### `/save` 커맨드

`~/.claude/commands/save.md` 파일을 생성하고 아래 내용을 작성합니다.

파일 내용 요약:

1. `cat last_save_marker.txt` 로 마지막 저장 시점 확인
   - 파일 있으면 → 해당 시점 이후 대화만 분석
   - 파일 없으면 → 전체 대화 분석 (첫 저장)
2. 아래 JSON 구조로 대화 내용 정리
   - `title`: 핵심 주제 + 이모지
   - `one_line_summary`: 한 문장 요약
   - `topics`: 다룬 주제 목록
   - `sections`: 주제별 `heading`(이모지 포함) + `overview` + `points`
   - `conclusion`: 결론
   - `next_steps`: 다음 할 일 (없으면 빈 배열)
3. `python main.py << 'ENDJSON' ... ENDJSON` 으로 저장 실행

#### `/reset-save` 커맨드

`~/.claude/commands/reset-save.md` 파일을 생성하고 아래 내용을 작성합니다.

파일 내용 요약:

1. `python main.py --reset` 실행
2. Notion에는 아무것도 저장하지 않고 현재 시점을 저장 기준점으로만 설정
3. 다음 `/save`부터 이 시점 이후 대화만 저장됨

## 사용 방법

### `/save`

Claude Code 대화 중 언제든지 입력:

```
/save
```

두 번째 저장부터는 마지막 저장 시점이 먼저 출력됩니다:

```
[마지막 저장] 2026-04-30 10:35 — 이전 대화 제목
Notion 저장 완료: https://...
```

### `/reset-save`

현재 대화 시점을 저장 기준점으로 설정합니다. Notion에는 아무것도 저장되지 않습니다.

```
/reset-save
```

활용 예시: 이전 대화는 기록하고 싶지 않고 지금부터 새롭게 저장을 시작하고 싶을 때 사용합니다. 다음 `/save`부터 이 시점 이후 대화만 Notion에 저장됩니다.

Notion에 생성되는 페이지 형식:

```
날짜: 2026-04-30 10:35
한줄 요약: 전체 대화를 한 문장으로 요약

────────────────────

📋 다룬 주제
• 주제 1
• 주제 2

────────────────────

🗂 정리

### 🔧 주제 1
한 문장 개요

• 핵심 포인트 1
• 핵심 포인트 2

────────────────────

✅ 결론
결론 및 결정된 사항

👉 다음 단계
• 다음에 할 일
```

## 에러 메시지

오류 발생 시 원인을 알 수 있는 한국어 메시지가 출력됩니다.

| 상황 | 원인 |
|------|------|
| `.env` 없음 또는 `NOTION_API_KEY` 미설정 | `.env.example` 참고하여 `.env` 생성 |
| `NOTION_PAGE_ID` 미설정 | `.env` 파일 확인 |
| JSON 형식 오류 | Claude가 생성한 JSON 구조 확인 |
| 401 Unauthorized | `NOTION_API_KEY` 값 확인 |
| 403 Forbidden | Notion 페이지에 Integration 연동 여부 확인 |
| 404 Not Found | `NOTION_PAGE_ID` 값 확인 |

## 의존 패키지

| 패키지 | 용도 |
|--------|------|
| `notion-client` | Notion API 공식 Python 클라이언트 |
| `python-dotenv` | `.env` 파일에서 환경 변수 로드 |
