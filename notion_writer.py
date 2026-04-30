import os
from datetime import datetime
from notion_client import Client


def create_page(title: str, one_line_summary: str, topics: list, sections: list, conclusion: str, next_steps: list) -> str:
    notion = Client(auth=os.environ["NOTION_API_KEY"])
    parent_id = os.environ["NOTION_PAGE_ID"]
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    children = []

    # 날짜 + 한줄 요약
    children += [
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"날짜: {today}"}}]
            },
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "한줄 요약: "}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": one_line_summary}},
                ]
            },
        },
        {"type": "divider", "divider": {}},
    ]

    # 다룬 주제 목록
    children.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "\U0001f4cb 다룬 주제"}}]},
    })
    for topic in topics:
        children.append({
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": topic}}]},
        })

    children.append({"type": "divider", "divider": {}})

    # 정리 섹션
    children.append({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "\U0001f5c2 정리"}}]},
    })

    for section in sections:
        # 주제 heading
        children.append({
            "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": section["heading"]}}]},
        })
        # 한 줄 개요
        children.append({
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": section["overview"]}}]
            },
        })
        # 핵심 bullet points
        for point in section["points"]:
            children.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": point}}]},
            })

    children.append({"type": "divider", "divider": {}})

    # 결론
    children += [
        {
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "✅ 결론"}}]},
        },
        {
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": conclusion}}]},
        },
    ]

    # 다음 단계
    if next_steps:
        children.append({
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "👉 다음 단계"}}]},
        })
        for step in next_steps:
            children.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": step}}]},
            })

    response = notion.pages.create(
        parent={"type": "page_id", "page_id": parent_id},
        properties={
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        children=children[:100],
    )

    for i in range(100, len(children), 100):
        notion.blocks.children.append(
            block_id=response["id"],
            children=children[i:i + 100],
        )

    return response["url"]
