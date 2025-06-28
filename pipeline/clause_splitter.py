import re

def split_clauses(text: str) -> list:
    """
    Splits a legal document text into clauses.
    Each clause is assumed to end with a period, newline, or semicolon.
    """

    # Clean up whitespace
    cleaned_text = re.sub(r'\n+', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Split by clause delimiters (can improve later)
    raw_clauses = re.split(r'(?<=[.;])\s+(?=[A-Z])', cleaned_text)

    # Filter out very short lines or empty ones
    clauses = [clause.strip() for clause in raw_clauses if len(clause.strip()) > 30]

    return clauses
