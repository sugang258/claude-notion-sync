import io
import json
import sys
from dotenv import load_dotenv
from notion_writer import create_page

load_dotenv()


def main():
    data = json.load(io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"))
    url = create_page(
        title=data["title"],
        one_line_summary=data["one_line_summary"],
        topics=data["topics"],
        sections=data["sections"],
        conclusion=data["conclusion"],
        next_steps=data.get("next_steps", []),
    )
    sys.stdout.buffer.write(f"Notion 저장 완료: {url}\n".encode("utf-8"))


if __name__ == "__main__":
    main()
