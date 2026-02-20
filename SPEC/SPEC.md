# Agent Specification: Research & Delivery Agent (ADK-Native)

## 1. Project Summary
Construction of a **dynamic autonomous intelligence agent** built with **Google ADK**. The agent is designed to discover, curate, and synthesize information across three specific **Content Pillars**, delivering a high-fidelity technical report via **Resend**. The system acts as a **strategic filter**, utilizing a curated list of authority sources to transform global information noise into actionable intelligence. The agent remains idle until **manually triggered** by the user via a Command Line Interface (CLI).

---

## 2. Identity and Persona (`adk.Agent`)
* **Agent Name:** Research & Delivery Agent.
* **Role:** Expert Trend Research Analyst.
* **Psychological Profile:** Analytical, pragmatic, and concise. It bypasses marketing "hype" to focus on technical implementation, feasibility, and real-world impact.
* **Communication Style:** Professional with "engineering wit"—utilizing analogies (hardware/software, technical debt, latency) to clarify complex concepts.
* **Objective:** Identify and synthesize exactly the **3 most disruptive advances per pillar** using high-signal authority sources upon manual request.

---

## 3. Dynamic Content Pillars & Authority Sources

| Pillar | Focus Area | Authority Sources |
| :--- | :--- | :--- |
| **1. Tech News** | Strategic moves from Big Tech (Google, NVIDIA, OpenAI, etc.) and global AI infrastructure. | TechCrunch (AI), The Verge, CNBC Tech. |
| **2. Product Engineering** | AI-Native products, production-ready architectures, and implementation insights. | VentureBeat, Towards Data Science, Papers with Code, Hacker News. |
| **3. Agentic AI & Frameworks** | Orchestration, design patterns (ReAct/Planning), ADK, and multi-agent systems. | Hacker News, ArXiv (cs.AI), Papers with Code. |

---

## 4. Tool Architecture (`adk.Tool`)

* **`HackerNewsConnector`:** Official Firebase API interface to extract top technical stories and trending discussions.
* **`TechAuthorityScraper`:** Specialized scraper for TechCrunch, VentureBeat, and The Verge, focusing on strategic headlines and technical deep-dives.
* **`ArXivConnectorTool`:** Interface to search and parse technical abstracts from the arXiv repository (specifically the `cs.AI` category).
* **`CodeInsightsTool`:** Integration with *Papers with Code* to extract implementation details and associated repositories for the Product Engineering pillar.
* **`PersistenceTool` (ADK InMemory):** Internal state management to track processed news IDs during the session, ensuring zero duplication in the final report.
* **`ResendEmailTool`:** Delivery tool that formats the synthesized intelligence into a professional HTML payload and sends it via the **Resend API**.

---

## 5. Policies and Constraints (`adk.Policy`)

* **`RelevanceThresholdPolicy`:** Each item is scored (1-10). Only items with a score > 8 (High Signal) are processed.
* **`PillarBalancePolicy`:** The agent **must** select exactly **3 items per pillar**, resulting in a total of 9 findings per report.
* **`ArchitectureRequirementPolicy`:** For the *Product Engineering* pillar, the agent **must** infer or extract the technical architecture of the products analyzed.
* **`ManualTriggerPolicy`:** The agent only initiates its workflow upon explicit user command via CLI.

---

## 6. Agentic Workflow (The Loop)

1.  **Trigger:** Manual CLI execution by the user.
2.  **Planning:** The agent maps the three active pillars to their respective authority sources.
3.  **Discovery:** Parallel invocation of connectors (`HackerNews`, `ArXiv`, `TechScrapers`).
4.  **Curation:**
    * Cross-reference findings with `InMemoryPersistence`.
    * Scoring and selection of the **Top 3 findings for each individual pillar**.
5.  **Technical Synthesis:** Generation of content: **TL;DR + Deep Dive (Architecture) + Engineering Analogy** for each of the 9 selected items.
6.  **Delivery:** Formatting into a structured HTML newsletter and transmission via `ResendEmailTool`.

---

## 7. Output Structure (Resend HTML Template)
* **Subject:** ☕ Intelligence Report | [Date] | [Top Signal Headline]
* **Sender:** `Research & Delivery Agent <onboarding@resend.dev>`

### Content Sections:
* **Section 1: The Big Picture (TL;DR):** 3 high-impact bullets summarizing the global landscape.
* **Section 2: Tech News (Top 3):** Analysis of strategic movements and infrastructure.
* **Section 3: Product Engineering (Top 3):** Breakdown of AI products and their inferred technical architectures.
* **Section 4: Agentic AI & Frameworks (Top 3):** Insights into orchestration, patterns, and new frameworks.

---

## 8. Suggested Tech Stack
* **Orchestrator:** Google ADK.
* **Model:** Gemini 3 Flash.
* **State Management:** **ADK InMemory Provider**.
* **Delivery Engine:** **Resend API**.
* **Environment:** Manual CLI / Local Python Environment.
* **Version Control:** GitHub.