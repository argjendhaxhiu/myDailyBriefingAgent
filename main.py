"""
Entry point. Run this with: python main.py
"""

from dotenv import load_dotenv
load_dotenv()  # must run before any other import that reads env vars

from agent import run_agent
from email_sender import send_briefing

# Your personal topics. Edit these freely.
TOPICS = [
    "legal tech software engineering programming UK 2026",
    "Kosovo latest political news 2026",
    "Premier Padel scores results rule changes 2026",
    "programming languages frameworks developer tools 2026",
    "AI models research releases 2026",
    "big tech industry news 2026",
]

if __name__ == "__main__":
    briefing = run_agent(TOPICS)
    print(briefing)

    with open("briefing.md", "w") as f:
        f.write(briefing)
    print("\nSaved to briefing.md")

    send_briefing(briefing)
