"""
CONCEPT: The agent loop.

This is the heart of every AI agent. The pattern is always:
  1. Send messages to Claude (including available tools)
  2. Claude either replies with text (done) or asks to use a tool
  3. If tool use: run the tool, add the result to messages, go to step 1
  4. If text: you have your final answer

This loop is what makes it an "agent" vs a single API call.
Claude decides how many searches to do, what to search for, when to stop.
"""

import os
import json
from datetime import date
import anthropic
from tools import TOOLS, run_tool


def run_agent(topics: list[str]) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    today = date.today().strftime("%B %d, %Y")  # e.g. "May 18, 2026"

    # The system prompt shapes Claude's behavior for the entire session.
    # Be specific: role, task, output format.
    system_prompt = f"""You are a personal news researcher for Argjend, who works in legal tech in Kosovo.
Today's date is {today}. Search results are pre-filtered to the last 24 hours only -- do not include older articles.

Context about Argjend's interests and priorities:
- Legal tech: focus on software engineering and programming within legal tech, and the UK scene specifically
- Kosovo: general news, latest political developments in Kosovo
- Padel: Premier Padel scores, results, rule changes, or major news only -- skip minor gossip
- Tech: prioritise (1) programming languages and developer tools, (2) AI models and research, (3) big tech industry news

Your job:
1. Search for today's news on each topic you are given
2. For each topic, pick the 3 most relevant and interesting results
3. Write a clean daily briefing in this format:

## Daily Briefing

### [Topic Name]
- **[Article title]** ([url])
  [2-sentence summary of why this matters]

Keep summaries concise. Flag anything directly relevant to Kosovo, Albania, or the EU legal space."""

    # Start the conversation with the user's request.
    # We build the full topic list into the first message.
    topic_list = "\n".join(f"- {t}" for t in topics)
    messages = [
        {
            "role": "user",
            "content": f"Please research and summarize today's news for these topics:\n{topic_list}"
        }
    ]

    print("Agent starting...\n")

    # THE LOOP
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )

        # CONCEPT: stop_reason tells you why Claude stopped generating.
        # "tool_use"  = Claude wants to call a tool, keep looping
        # "end_turn"  = Claude is done, extract the text and return it

        if response.stop_reason == "end_turn":
            # Extract the text content from the final response
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text

        elif response.stop_reason == "tool_use":
            # Add Claude's response (which contains the tool request) to history
            messages.append({"role": "assistant", "content": response.content})

            # Process every tool call Claude made (it can request multiple at once)
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  Searching: {block.input.get('query', '')}")

                    result = run_tool(block.name, block.input)

                    # CONCEPT: tool results go back to Claude as a "user" message.
                    # Claude reads these results and decides what to do next.
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })

            messages.append({"role": "user", "content": tool_results})

        else:
            # Unexpected stop reason -- surface it so you can debug
            raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")
