import io
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MARKER_FILE = os.path.join(os.path.dirname(__file__), "last_save_marker.txt")


def err(msg: str):
    sys.stderr.buffer.write(f"오류: {msg}\n".encode("utf-8"))
    sys.exit(1)


def read_marker():
    if not os.path.exists(MARKER_FILE):
        return None
    with open(MARKER_FILE, encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    return {"saved_at": lines[0], "title": lines[1]} if len(lines) >= 2 else None


def write_marker(title: str):
    with open(MARKER_FILE, "w", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n{title}")


def reset():
    write_marker("(수동 리셋)")
    sys.stdout.buffer.write(
        f"리셋 완료: 다음 /save부터 현재 시점 이후 대화만 저장됩니다.\n".encode("utf-8")
    )


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset()
        return

    # 환경 변수 확인
    if not os.environ.get("NOTION_API_KEY"):
        err(".env 파일이 없거나 NOTION_API_KEY가 설정되지 않았습니다. .env.example을 참고해 생성해주세요.")
    if not os.environ.get("NOTION_PAGE_ID"):
        err("NOTION_PAGE_ID가 설정되지 않았습니다. .env 파일을 확인해주세요.")

    marker = read_marker()
    if marker:
        msg = f"[마지막 저장] {marker['saved_at']} — {marker['title']}\n"
        sys.stdout.buffer.write(msg.encode("utf-8"))

    # JSON 파싱
    try:
        data = json.load(io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"JSON 형식이 잘못됐습니다. ({e})")

    # Notion API 호출
    try:
        from notion_writer import create_page
        url = create_page(
            title=data["title"],
            one_line_summary=data["one_line_summary"],
            topics=data["topics"],
            sections=data["sections"],
            conclusion=data["conclusion"],
            next_steps=data.get("next_steps", []),
        )
    except Exception as e:
        msg = str(e)
        if "401" in msg:
            err("Notion API 키가 유효하지 않습니다. .env의 NOTION_API_KEY를 확인해주세요.")
        elif "404" in msg:
            err("Notion 페이지를 찾을 수 없습니다. NOTION_PAGE_ID를 확인해주세요.")
        elif "403" in msg:
            err("페이지 접근 권한이 없습니다. Notion 페이지에 Integration이 연동되었는지 확인해주세요.")
        else:
            err(f"Notion 저장 중 오류가 발생했습니다. ({msg})")

    write_marker(data["title"])
    sys.stdout.buffer.write(f"Notion 저장 완료: {url}\n".encode("utf-8"))


if __name__ == "__main__":
    main()
