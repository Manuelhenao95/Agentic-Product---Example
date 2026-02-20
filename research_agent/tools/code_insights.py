"""CodeInsightsTool — Fetches trending papers and repos from Papers with Code."""

import httpx


def get_code_insights(query: str = "artificial intelligence") -> dict:
    """Searches Papers with Code for trending papers with linked repositories.

    Queries the Papers with Code API to find papers that have associated
    GitHub repositories, providing insights into production-ready
    implementations and their technical stack.

    Args:
        query: Search terms for finding relevant papers and code
               (e.g. 'transformer', 'multimodal', 'agent framework').

    Returns:
        dict: A dictionary with 'status' and 'papers' list containing
              title, abstract, url, repository URL, stars, and framework.
    """
    BASE = "https://paperswithcode.com/api/v1"

    try:
        with httpx.Client(timeout=30) as client:
            # Search for papers
            resp = client.get(
                f"{BASE}/search/",
                params={"q": query, "page": 1, "items_per_page": 15},
            )
            resp.raise_for_status()
            data = resp.json()

            results = data.get("results", [])
            papers = []

            for item in results:
                paper = item.get("paper", {})
                if not paper:
                    continue

                # Try to get repository info
                paper_id = paper.get("id", "")
                repo_url = ""
                stars = 0
                framework = "Unknown"

                if paper_id:
                    try:
                        repo_resp = client.get(
                            f"{BASE}/papers/{paper_id}/repositories/"
                        )
                        if repo_resp.status_code == 200:
                            repos = repo_resp.json().get("results", [])
                            if repos:
                                top_repo = repos[0]
                                repo_url = top_repo.get("url", "")
                                stars = top_repo.get("stars", 0)
                                framework = top_repo.get("framework", "Unknown")
                    except Exception:
                        pass  # Repo info is optional

                abstract = paper.get("abstract", "")
                if len(abstract) > 500:
                    abstract = abstract[:497] + "..."

                papers.append({
                    "title": paper.get("title", "No title"),
                    "abstract": abstract,
                    "paper_url": paper.get("url_abs", ""),
                    "repo_url": repo_url,
                    "stars": stars,
                    "framework": framework,
                })

            return {
                "status": "success",
                "source": "Papers with Code",
                "total_results": len(papers),
                "papers": papers,
            }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
