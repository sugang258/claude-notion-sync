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
        summary=data["summary"],
        questions=data["questions"],
        conclusion=data["conclusion"],
    )
    sys.stdout.buffer.write(f"Notion 저장 완료: {url}\n".encode("utf-8"))


if __name__ == "__main__":
    main()
