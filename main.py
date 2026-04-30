import io
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from notion_writer import create_page

load_dotenv()

MARKER_FILE = os.path.join(os.path.dirname(__file__), "last_save_marker.txt")


def read_marker():
    if not os.path.exists(MARKER_FILE):
        return None
    with open(MARKER_FILE, encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    return {"saved_at": lines[0], "title": lines[1]} if len(lines) >= 2 else None


def write_marker(title: str):
    with open(MARKER_FILE, "w", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n{title}")


def main():
    marker = read_marker()
    if marker:
        msg = f"[마지막 저장] {marker['saved_at']} — {marker['title']}\n"
        sys.stdout.buffer.write(msg.encode("utf-8"))

    data = json.load(io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"))
    url = create_page(
        title=data["title"],
        one_line_summary=data["one_line_summary"],
        topics=data["topics"],
        sections=data["sections"],
        conclusion=data["conclusion"],
        next_steps=data.get("next_steps", []),
    )
    write_marker(data["title"])
    sys.stdout.buffer.write(f"Notion 저장 완료: {url}\n".encode("utf-8"))


if __name__ == "__main__":
    main()
