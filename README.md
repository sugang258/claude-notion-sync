# Claude → Notion 연동 시스템

Claude Code 대화를 `/save` 명령어 한 번으로 Notion 페이지에 자동 정리하는 시스템입니다.

## 개요

| 항목 | 내용 |
|------|------|
| 트리거 | `/save` 명령어 입력 시 |
| 저장 범위 | 현재 대화 전체 |
| 저장 형식 | 제목 / 날짜 / 한줄 요약 / 다룬 주제 / 정리 / 결론 / 다음 단계 |
| 기술 스택 | Python + Notion API |

## 파일 구조

```
claude-notion-sync/
├── main.py            # 실행 진입점 (JSON stdin → Notion 저장)
├── notion_writer.py   # Notion API 블록 생성 및 페이지 작성
├── requirements.txt   # 의존 패키지
├── .env               # API 키 (직접 생성 필요, git 제외)
└── .env.example       # 환경 변수 형식 안내

~/.claude/commands/
└── save.md            # /save 슬래시 커맨드 정의 (전역)
```

## 동작 흐름

```
사용자가 /save 입력
    ↓
Claude가 대화 내용 분석 → JSON 생성
    ↓
echo 'JSON' | python main.py 실행
    ↓
notion_writer.py → Notion API 호출
    ↓
Notion 부모 페이지 아래 새 자식 페이지 생성 → URL 출력
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

### 6. `/save` 슬래시 커맨드 등록

`~/.claude/commands/save.md` 파일 생성:

```markdown
지금까지의 대화를 분석하여 Notion에 저장하세요.

다음 단계를 순서대로 실행하세요:

1. 대화 내용을 바탕으로 아래 JSON을 작성하세요:
   - title: 대화 핵심 주제 (간결하게, 한 줄)
   - one_line_summary: 전체 대화를 한 문장으로 요약
   - topics: 대화에서 다룬 주제 목록 (짧게, 배열)
   - sections: 각 주제별 정리
     - heading: 주제명
     - overview: 이 주제에서 무슨 일이 있었는지 한 문장 개요
     - points: 핵심 사항을 짧고 명확하게 bullet 형태로
   - conclusion: 대화를 통해 결정되거나 확인된 사항
   - next_steps: 다음에 할 일 목록 (없으면 빈 배열)

2. 아래 명령어를 실행하여 Notion에 저장하세요 (JSON을 실제 내용으로 채워서):

```bash
python /path/to/claude-notion-sync/main.py << 'ENDJSON'
{"title":"...", "one_line_summary":"...", "topics":["..."], "sections":[{"heading":"...","overview":"...","points":["...","..."]}], "conclusion":"...", "next_steps":["..."]}
ENDJSON
```

저장 완료 후 Notion 페이지 URL을 알려주세요.
```

## 사용 방법

Claude Code 대화 중 언제든지 입력:

```
/save
```

Claude가 자동으로 대화를 분석하고 Notion에 아래 형식으로 저장합니다.

```
날짜: 2026-04-30
한줄 요약: 전체 대화를 한 문장으로 요약

────────────────────

## 다룬 주제
• 주제 1
• 주제 2

────────────────────

## 정리

### 주제 1
한 문장 개요

• 핵심 포인트 1
• 핵심 포인트 2

### 주제 2
한 문장 개요

• 핵심 포인트 1
• 핵심 포인트 2

────────────────────

## 결론
결론 및 결정된 사항

## 다음 단계
• 다음에 할 일
```

## 의존 패키지

| 패키지 | 용도 |
|--------|------|
| `notion-client` | Notion API 공식 Python 클라이언트 |
| `python-dotenv` | `.env` 파일에서 환경 변수 로드 |
