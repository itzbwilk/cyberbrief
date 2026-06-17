## CyberBrief - Automated Daily Cybersecurity Update to Notion
A Python automation project that fetches current events in cybersecurity every morning and analyzes it using OpenAI's GPT-4o-mini model with web search. Results are automatically posted as a structured threat intelligence brief to Notion with no manual input required.

## What It Does
- Runs daily at 5:00AM via Windows Task Scheduler
- Pulls real cybersecurity stories from Bleeping Computer, The Hacker News and SecurityWeek
- Generates a structured CyberBrief with severity rating, takeaways and source URLs
- Automatically updates a Notion page with the daily brief

## Key Lessons Learned

- The OpenAI web search tool can find real article titles and summaries reliably, 
  but does not consistently return accurate deep-link URLs and it sometimes 
  fabricates plausible-looking links or returns generic homepage URLs instead.
- Fixed by restructuring the pipeline: Python fetches real articles directly from 
  each source's RSS feed (BleepingComputer, The Hacker News, SecurityWeek) using 
  `feedparser`, guaranteeing accurate titles, sources, and URLs with zero AI 
  involvement in the citation itself. GPT is only used to write analysis on top 
  of this verified data, never to generate or recall a link.
- RSS feeds for BleepingComputer and SecurityWeek block requests without a 
  proper browser User-Agent header. This required spoofing a Chrome user agent to 
  fetch successfully.
- General principle: when an AI tool is asked to both retrieve information and 
  format/cite it precisely, it can prioritize satisfying the format over factual 
  accuracy. Separating data retrieval (code) from analysis (AI) produces more 
  reliable, trustworthy automation.

## Tech Stack
- Python 3.14
- OpenAI API (GPT-4o-mini, used for analysis/writing)
- feedparser (RSS feed parsing for verified article data)
- Notion API
- Windows Task Scheduler
- python-dotnev for secret management

## Skills Demonstrated
- REST API integration and authentication
- Secure credential management with environment variables
- Automated task scheduling on Windows
- Python scripting and error handling

## Setup
1. Clone the repo
2. Create a virtual environment and install dependencies:
   pip install openai notion-client python-dotnev
3. Create a .env file with your credentials (see .env example)
4. Connect your Notion integration to your target page
5. Schedule cyberbrief.py with Windows Task Scheduler

## Environment Variables
Create a .env file in project root:
OPENAI_API_KEY=your_key_here
NOTION_TOKEN=your_token_here
NOTION_PAGE_ID=your_page_id_here

## Author
Brandon - Cybersecurity Student at MSU Denver | Cybersecurity Intern at United Launch Alliance
