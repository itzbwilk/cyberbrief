import os
from openai import OpenAI
from notion_client import Client
from datetime import date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
notion = Client(auth=os.getenv("NOTION_TOKEN"))
PAGE_ID = os.getenv("NOTION_PAGE_ID")

today = date.today().strftime("%B %d, %Y")

prompt = f"""
You are a cybersecurity analyst writing a daily brief for a cybersecurity intern 
focused on incident response and malware analysis at a defense contractor.

Search the web for today's ({today}) top 3 REAL cybersecurity news stories. 
Use exactly ONE story from each of these sources:
- BleepingComputer (bleepingcomputer.com)
- The Hacker News (thehackernews.com)
- SecurityWeek (securityweek.com)

Only use real, verified stories with actual source URLs. Do not fabricate stories.

Write a CyberBrief using EXACTLY this format — no markdown hyperlinks, just plain URLs:

# 🛡️ CyberBrief — {today}

## Story 1: [Real Title]
Source: [Publication Name]
URL: [plain URL only, no brackets or markdown]
Severity: 🔴 CRITICAL / 🟠 HIGH / 🟡 MEDIUM (pick one)
Summary: 2-3 sentence summary of what actually happened.
Why it matters for you: 1-2 sentences connecting this to IR/malware analysis work.
Takeaway: One concrete action or lesson.

## Story 2: [Real Title]
(same format)

## Story 3: [Real Title]
(same format)

---

## 📚 Term of the Day
**[Term]:** Definition and why it matters in security operations.

## 🔗 Internship Connection
One paragraph connecting today's stories to real SOC/IR analyst work, 
referencing tools like Splunk, Microsoft Defender, or Trellix where relevant.
"""

# Call OpenAI API with web search enabled
response = openai_client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search_preview"}],
    input=prompt
)

# Extract the text output
brief_content = ""
for item in response.output:
    if hasattr(item, "content"):
        for block in item.content:
            if hasattr(block, "text"):
                brief_content += block.text

# Convert markdown to Notion blocks
def text_to_notion_blocks(text):
    blocks = []
    lines = text.split('\n')
    
    for line in lines:
        if not line.strip():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            })
        elif line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}
            })
        elif line.startswith('---'):
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })
        else:
            clean_line = line.replace('**', '')
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": clean_line}}]}
            })
    
    return blocks

# Clear existing content and replace with today's brief
def update_notion_page(content):
    existing = notion.blocks.children.list(block_id=PAGE_ID)
    
    for block in existing.get("results", []):
        notion.blocks.delete(block_id=block["id"])
    
    blocks = text_to_notion_blocks(content)
    
    chunk_size = 100
    for i in range(0, len(blocks), chunk_size):
        chunk = blocks[i:i + chunk_size]
        notion.blocks.children.append(block_id=PAGE_ID, children=chunk)
    
    print(f"✅ CyberBrief for {today} successfully posted to Notion.")

# Run it
update_notion_page(brief_content)
