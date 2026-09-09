"""Batch number formatting for Label Traxx job/item pairs (see QUESTIONS.md #1)."""


def build_batch_number(job_number: str, item_number: str) -> str:
    """Job number followed directly by item number, no separator."""
    return f"{job_number}{item_number}"
