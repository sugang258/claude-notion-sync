import json
import sys
from dotenv import load_dotenv
from notion_writer import create_page

load_dotenv()


def main():
    data = json.load(sys.stdin)
    url = create_page(
        title=data["title"],
        summary=data["summary"],
        questions=data["questions"],
        conclusion=data["conclusion"],
    )
    print(f"✅ Notion 저장 완료: {url}")


if __name__ == "__main__":
    main()
