"""HackerNewsConnector — Fetches top tech/AI stories from the HN Firebase API."""

import httpx


def search_hacker_news(query: str = "AI") -> dict:
    """Searches Hacker News for top stories related to a query.

    Connects to the official Hacker News Firebase API, retrieves the current
    top stories, and filters them by keyword relevance.

    Args:
        query: Search keyword to filter stories (e.g. 'AI', 'LLM', 'agent').

    Returns:
        dict: A dictionary with 'status' and 'stories' list containing
              id, title, url, score, and num_comments for each match.
    """
    BASE = "https://hacker-news.firebaseio.com/v0"

    try:
        with httpx.Client(timeout=30) as client:
            # Get top 100 story IDs
            resp = client.get(f"{BASE}/topstories.json")
            resp.raise_for_status()
            story_ids = resp.json()[:100]

            stories = []
            keywords = [kw.strip().lower() for kw in query.split(",")]

            for sid in story_ids:
                item = client.get(f"{BASE}/item/{sid}.json").json()
                if item is None:
                    continue

                title = (item.get("title") or "").lower()
                # Check if any keyword matches the title
                if any(kw in title for kw in keywords):
                    stories.append({
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                        "score": item.get("score", 0),
                        "num_comments": item.get("descendants", 0),
                    })

                if len(stories) >= 15:
                    break

        return {
            "status": "success",
            "source": "Hacker News",
            "total_results": len(stories),
            "stories": stories,
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
