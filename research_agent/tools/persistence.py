"""PersistenceTool — In-session deduplication using ADK tool context state."""

from google.adk.tools import ToolContext


def check_duplicate(item_id: str, tool_context: ToolContext) -> dict:
    """Checks if a news item has already been processed in this session.

    Uses the ADK session state to track which item IDs have already been
    processed, preventing duplicate entries in the final report.

    Args:
        item_id: Unique identifier for the news item to check.

    Returns:
        dict: A dictionary with 'is_duplicate' (bool) indicating if the
              item was already processed, and the item_id.
    """
    processed = tool_context.state.get("processed_ids", [])
    is_dup = item_id in processed

    return {
        "item_id": item_id,
        "is_duplicate": is_dup,
    }


def mark_processed(item_id: str, tool_context: ToolContext) -> dict:
    """Marks a news item as processed in the session state.

    Adds the item ID to the processed list in the ADK session state,
    ensuring it will be flagged as a duplicate in future checks.

    Args:
        item_id: Unique identifier for the news item to mark.

    Returns:
        dict: A dictionary confirming the item was marked as processed.
    """
    processed = tool_context.state.get("processed_ids", [])
    if item_id not in processed:
        processed.append(item_id)
        tool_context.state["processed_ids"] = processed

    return {
        "item_id": item_id,
        "marked": True,
        "total_processed": len(processed),
    }
