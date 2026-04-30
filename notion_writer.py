import os
from datetime import datetime
from notion_client import Client


def create_page(title: str, summary: str, questions: list, conclusion: str) -> str:
    notion = Client(auth=os.environ["NOTION_API_KEY"])
    parent_id = os.environ["NOTION_PAGE_ID"]
    today = datetime.now().strftime("%Y-%m-%d")

    children = [
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"날짜: {today}"}}]
            },
        },
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "요약"}}]
            },
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": summary}}]
            },
        },
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "주요 질문"}}]
            },
        },
    ]

    for q in questions:
        children.append({
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": q}}]
            },
        })

    children += [
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "결론"}}]
            },
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": conclusion}}]
            },
        },
    ]

    response = notion.pages.create(
        parent={"type": "page_id", "page_id": parent_id},
        properties={
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        children=children,
    )
    return response["url"]
