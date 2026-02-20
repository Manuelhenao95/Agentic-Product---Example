"""Research & Delivery Agent — Root agent definition for Google ADK."""

from google.adk.agents import Agent

from .prompt import SYSTEM_INSTRUCTION
from .tools.hacker_news import search_hacker_news
from .tools.tech_scraper import scrape_tech_sources
from .tools.arxiv_connector import search_arxiv
from .tools.code_insights import get_code_insights
from .tools.persistence import check_duplicate, mark_processed
from .tools.resend_email import send_report_email


root_agent = Agent(
    name="research_delivery_agent",
    model="gemini-3-flash-preview",
    description=(
        "An autonomous intelligence agent that discovers, curates, and "
        "synthesizes information across Tech News, Product Engineering, "
        "and Agentic AI pillars, delivering a professional HTML report "
        "via Resend email."
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        search_hacker_news,
        scrape_tech_sources,
        search_arxiv,
        get_code_insights,
        check_duplicate,
        mark_processed,
        send_report_email,
    ],
)
