import re


def extract_sections(proposal_text: str):
    """
    Extracts major proposal sections using keyword-based detection.
    Works for most R&D proposal PDFs.
    """

    sections = {
        "Objectives": "",
        "Methodology": "",
        "Innovation": "",
        "Expected Impact": "",
        "Risk & Feasibility": ""
    }

    patterns = {
        "Objectives": r"(objectives|aim|goal)(.*?)(methodology|approach|innovation)",
        "Methodology": r"(methodology|approach)(.*?)(innovation|impact|expected outcome)",
        "Innovation": r"(innovation|novelty)(.*?)(impact|expected outcome|risk)",
        "Expected Impact": r"(impact|expected outcome)(.*?)(risk|feasibility|budget)",
        "Risk & Feasibility": r"(risk|feasibility)(.*)"
    }

    text = proposal_text.lower()

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections[key] = match.group(2)[:1200]

    return sections
