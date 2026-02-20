#!/usr/bin/env python3
"""Research & Delivery Agent — CLI Entry Point.

Manual trigger for the intelligence agent. Executes the full agentic
workflow: discovery → curation → synthesis → delivery.

Usage:
    python main.py
"""

import asyncio
import os

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Load environment variables BEFORE importing the agent
load_dotenv()

from research_agent.agent import root_agent  # noqa: E402


TRIGGER_PROMPT = (
    "Execute your full intelligence gathering workflow now. "
    "Discover the latest advances across all three pillars "
    "(Tech News, Product Engineering, Agentic AI & Frameworks), "
    "curate the top 3 findings per pillar, synthesize your analysis, "
    "and deliver the report via email."
)


async def main():
    """Run the Research & Delivery Agent."""
    print("=" * 60)
    print("☕ Research & Delivery Agent")
    print("=" * 60)
    print(f"Model: gemini-3-flash-preview")
    print(f"Recipient: {os.getenv('RECIPIENT_EMAIL', 'Not set')}")
    print("-" * 60)
    print("🚀 Triggering agent workflow...\n")

    # Create session service and runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="research_delivery_agent",
        session_service=session_service,
    )

    # Create a new session
    session = await session_service.create_session(
        app_name="research_delivery_agent",
        user_id="cli_user",
    )

    # Build the user message
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=TRIGGER_PROMPT)],
    )

    # Run the agent and stream events
    print("📡 Agent is working...\n")

    async for event in runner.run_async(
        user_id="cli_user",
        session_id=session.id,
        new_message=user_message,
    ):
        # Display agent's text responses
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)
                if part.function_call:
                    print(f"  🔧 Calling: {part.function_call.name}()")
                if part.function_response:
                    status = "✅" if "success" in str(part.function_response) else "⚠️"
                    print(f"  {status} Response from: {part.function_response.name}")

    print("\n" + "-" * 60)
    print("✅ Agent workflow completed.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
