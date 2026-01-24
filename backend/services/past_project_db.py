import pandas as pd

def load_past_projects():
    """
    Loads NaCCER past/ongoing projects dataset.

    CSV must contain at least:
    - title
    - objective
    - domain

    File: data/past_projects.csv
    """

    df = pd.read_csv("data/past_projects.csv")

    projects = []
    for _, row in df.iterrows():
        projects.append({
            "title": row["title"],
            "objective": row["objective"],
            "domain": row.get("domain", "Coal R&D")
        })

    return projects
