"""TechAuthorityScraper — Fetches headlines from tech RSS feeds."""

import feedparser


# Curated RSS feeds for each authority source
RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "CNBC Tech": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910",
}


def scrape_tech_sources(sources: str = "all") -> dict:
    """Scrapes technology news from authoritative RSS feeds.

    Fetches and parses RSS feeds from TechCrunch, The Verge, VentureBeat,
    and CNBC Tech to collect the latest AI and technology headlines.

    Args:
        sources: Comma-separated list of sources to scrape, or 'all'.
                 Valid sources: 'TechCrunch AI', 'The Verge AI',
                 'VentureBeat AI', 'CNBC Tech'.

    Returns:
        dict: A dictionary with 'status' and 'articles' list containing
              source, title, summary, url, and published date.
    """
    try:
        feeds_to_parse = RSS_FEEDS
        if sources.lower() != "all":
            requested = [s.strip() for s in sources.split(",")]
            feeds_to_parse = {
                k: v for k, v in RSS_FEEDS.items() if k in requested
            }

        articles = []

        for source_name, feed_url in feeds_to_parse.items():
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:10]:
                # Extract summary, handling different RSS formats
                summary = ""
                if hasattr(entry, "summary"):
                    summary = entry.summary
                elif hasattr(entry, "description"):
                    summary = entry.description

                # Strip HTML tags from summary
                import re
                summary = re.sub(r"<[^>]+>", "", summary).strip()
                # Truncate to 500 chars
                if len(summary) > 500:
                    summary = summary[:497] + "..."

                articles.append({
                    "source": source_name,
                    "title": entry.get("title", "No title"),
                    "summary": summary,
                    "url": entry.get("link", ""),
                    "published": entry.get("published", "Unknown"),
                })

        return {
            "status": "success",
            "source": "Tech Authority RSS Feeds",
            "total_results": len(articles),
            "articles": articles,
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
