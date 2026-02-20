# ☕ Research & Delivery Agent

An autonomous intelligence agent built with **Google ADK** and **Gemini 3 Flash** that discovers, curates, and synthesizes information across three AI/Tech pillars, delivering a professional HTML report via **Resend**.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Google ADK](https://img.shields.io/badge/Google%20ADK-Agent%20Framework-orange)
![Gemini](https://img.shields.io/badge/Gemini%203-Flash%20Preview-green)

---

## 🧠 What It Does

When triggered via CLI, the agent autonomously:

1. **Discovers** — Pulls data from HackerNews, TechCrunch, VentureBeat, The Verge, arXiv (cs.AI), and Papers with Code
2. **Curates** — Scores each item (1-10) and selects the **Top 3 per pillar** (9 total)
3. **Synthesizes** — Generates TL;DR, Deep Dive (Architecture), and Engineering Analogy for each finding
4. **Delivers** — Sends a dark-themed HTML report via Resend email

### Content Pillars

| Pillar | Focus |
|:---|:---|
| 🔵 **Tech News** | Strategic moves from Big Tech and AI infrastructure |
| 🟢 **Product Engineering** | AI-native products and production architectures |
| 🟣 **Agentic AI & Frameworks** | Orchestration, design patterns, multi-agent systems |

---

## 🏗️ Architecture

```
main.py (CLI) → ADK Runner → research_delivery_agent
                                 ├── search_hacker_news()
                                 ├── scrape_tech_sources()
                                 ├── search_arxiv()
                                 ├── get_code_insights()
                                 ├── check_duplicate() / mark_processed()
                                 └── send_report_email() → report.html
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/Manuelhenao95/Agentic-Product---Example.git
cd Agentic-Product---Example
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```
GOOGLE_API_KEY=your_gemini_api_key
RESEND_API_KEY=your_resend_api_key
RECIPIENT_EMAIL=your_email@example.com
```

| Key | Get it from |
|:---|:---|
| `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) |
| `RESEND_API_KEY` | [Resend Dashboard](https://resend.com/api-keys) |

### 3. Run

```bash
python main.py
```

Or use the ADK Web UI for debugging:

```bash
adk web
```

---

## 📂 Project Structure

```
├── main.py                          # CLI entry point
├── requirements.txt                 # Dependencies
├── .env.example                     # API keys template
├── research_agent/
│   ├── __init__.py
│   ├── agent.py                     # Root ADK agent definition
│   ├── prompt.py                    # System instruction & persona
│   └── tools/
│       ├── hacker_news.py           # Hacker News Firebase API
│       ├── tech_scraper.py          # RSS feeds scraper
│       ├── arxiv_connector.py       # arXiv cs.AI search
│       ├── code_insights.py         # Papers with Code API
│       ├── persistence.py           # In-session deduplication
│       └── resend_email.py          # Email rendering & delivery
├── templates/
│   └── report.html                  # HTML email template
└── SPEC/
    └── SPEC.md                      # Original specification
```

---

## 🔧 Tech Stack

- **Orchestrator:** Google ADK
- **Model:** Gemini 3 Flash Preview
- **State:** ADK InMemory Session
- **Delivery:** Resend API
- **Template:** Jinja2

---

## 🔒 Security

- API keys are stored in `.env` (gitignored, **never committed**)
- `.env.example` provides a safe template for collaborators
- No hardcoded secrets in source code

---

## 📄 License

MIT
