"""ArXivConnectorTool — Searches and parses papers from arXiv cs.AI."""

import arxiv


def search_arxiv(query: str = "artificial intelligence", max_results: int = 15) -> dict:
    """Searches arXiv for recent papers in the cs.AI category.

    Queries the arXiv repository for papers matching the given search terms,
    sorted by submission date (most recent first). Focuses on the cs.AI
    (Artificial Intelligence) category.

    Args:
        query: Search terms for finding relevant papers
               (e.g. 'multi-agent systems', 'LLM reasoning').
        max_results: Maximum number of papers to return (default 15).

    Returns:
        dict: A dictionary with 'status' and 'papers' list containing
              title, authors, abstract, url, published date, and categories.
    """
    try:
        client = arxiv.Client()

        search = arxiv.Search(
            query=f"cat:cs.AI AND ({query})",
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        papers = []
        for result in client.results(search):
            # Truncate abstract
            abstract = result.summary
            if len(abstract) > 600:
                abstract = abstract[:597] + "..."

            papers.append({
                "title": result.title,
                "authors": ", ".join([a.name for a in result.authors[:5]]),
                "abstract": abstract,
                "url": result.entry_id,
                "published": result.published.strftime("%Y-%m-%d"),
                "categories": result.categories,
            })

        return {
            "status": "success",
            "source": "arXiv (cs.AI)",
            "total_results": len(papers),
            "papers": papers,
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
