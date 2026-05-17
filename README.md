# My Daily Summary News Agent

A simple AI agent that researches and summarizes daily news across your chosen topics.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
   - Get your Anthropic key at: https://console.anthropic.com
   - Get your Tavily key at: https://app.tavily.com (free tier available)

3. Run the agent:
   ```bash
   python main.py
   ```

## What each file teaches you

| File | Concept |
|------|---------|
| `tools.py` | How to define and implement tools (functions Claude can call) |
| `agent.py` | The agent loop: send, check stop_reason, run tools, repeat |
| `main.py` | Entry point, your personal config |

## How to extend this

- **Add a tool**: define it in `TOOLS` list in `tools.py`, implement the function, add a branch in `run_tool()`
- **Save to Notion / email yourself**: replace the file write in `main.py`
- **Run daily automatically**: add a cron job pointing to `python main.py`
- **Add memory**: store past briefings and have Claude notice trends over time
