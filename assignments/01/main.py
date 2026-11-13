"""Populate the assignment 1 database with random data.

Connection is taken from $DATABASE_URL (same variable dbmate uses),
falling back to the local `unifr_big_data` database.

Usage:
    uv run assignments/01/main.py [--seed N]
"""

import argparse
import os
import random
from datetime import date, timedelta

import psycopg2
from psycopg2.extras import execute_values

N_AUTHORS = 50
N_PAPERS = 100
N_CONFERENCES = 15

FIRST_NAMES = [
    "Alice", "Bruno", "Chloé", "David", "Elena", "Fabian", "Giulia", "Hugo",
    "Ines", "Jonas", "Klara", "Luca", "Mia", "Noah", "Olivia", "Pierre",
    "Quentin", "Rosa", "Samuel", "Tina", "Ursula", "Victor", "Wei", "Yuki",
]
LAST_NAMES = [
    "Müller", "Meier", "Schmid", "Keller", "Weber", "Huber", "Rossi", "Dubois",
    "Martin", "Bernard", "Fischer", "Wagner", "Zhang", "Tanaka", "Garcia",
    "Nguyen", "Smith", "Kowalski", "Novak", "Silva",
]
AFFILIATIONS = [
    "University of Fribourg", "ETH Zurich", "EPFL", "University of Bern",
    "University of Geneva", "TU Munich", "MIT", "Stanford University",
    "University of Oxford", "Inria", "Max Planck Institute", None,
]
CONFERENCES = [
    ("VLDB", "A*"), ("SIGMOD", "A*"), ("ICDE", "A*"), ("KDD", "A*"),
    ("EDBT", "A"), ("CIKM", "A"), ("WWW", "A*"), ("ICDM", "A*"),
    ("DASFAA", "A"), ("DEXA", "B"), ("ADBIS", "B"), ("SSDBM", "A"),
    ("BigData", "B"), ("DOLAP", "C"), ("BDA", "C"), ("ICWE", None),
]
TOPIC_ADJ = [
    "Scalable", "Distributed", "Efficient", "Adaptive", "Incremental",
    "Approximate", "Learned", "Robust", "Parallel", "Streaming",
]
TOPIC_NOUN = [
    "Query Processing", "Graph Analytics", "Index Structures", "Join Algorithms",
    "Data Cleaning", "Schema Matching", "Transaction Management",
    "Time Series Storage", "Entity Resolution", "Cardinality Estimation",
]
TOPIC_CONTEXT = [
    "in the Cloud", "for Big Data", "on Modern Hardware", "at Scale",
    "with Machine Learning", "over Data Lakes", "in NoSQL Systems", "",
]
ABSTRACT_SENTENCES = [
    "We present a novel approach to {topic}.",
    "Existing systems struggle with {topic} as data volumes grow.",
    "Our method reduces latency by up to {n}x compared to the state of the art.",
    "We evaluate our prototype on {m} real-world datasets.",
    "Experiments show significant improvements in throughput and memory usage.",
    "We formally prove the correctness of the proposed algorithm.",
    "Finally, we discuss open challenges and directions for future work.",
]


def get_connection():
    dsn = os.environ.get("DATABASE_URL", "dbname=unifr_big_data")
    return psycopg2.connect(dsn)


def random_title() -> str:
    parts = [random.choice(TOPIC_ADJ), random.choice(TOPIC_NOUN), random.choice(TOPIC_CONTEXT)]
    return " ".join(p for p in parts if p)


def random_abstract(title: str) -> str:
    sentences = random.sample(ABSTRACT_SENTENCES, k=random.randint(3, 5))
    return " ".join(
        s.format(topic=title.lower(), n=random.randint(2, 20), m=random.randint(2, 8))
        for s in sentences
    )


def random_date(start: date = date(2018, 1, 1), end: date = date(2025, 6, 1)) -> date:
    # end leaves room for up to 2 resubmissions (<= 400 days) without hitting the future
    return start + timedelta(days=random.randint(0, (end - start).days))


def insert_returning_ids(cur, sql: str, rows: list[tuple]) -> list[int]:
    return [r[0] for r in execute_values(cur, sql, rows, fetch=True)]


def populate(cur) -> None:
    # Start from a clean slate so the script can be re-run.
    cur.execute(
        "TRUNCATE Cites, Submits, Writes, Paper, Author, Conference RESTART IDENTITY CASCADE"
    )

    # --- Authors -----------------------------------------------------------
    authors = []
    for i in range(N_AUTHORS):
        first, last = random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
        email = f"{first}.{last}.{i}@example.org".lower()  # suffix keeps emails unique
        authors.append((f"{first} {last}", email, random.choice(AFFILIATIONS)))
    author_ids = insert_returning_ids(
        cur,
        "INSERT INTO Author (name, email, affiliation) VALUES %s RETURNING authorID",
        authors,
    )

    # --- Conferences -------------------------------------------------------
    confs = random.sample(CONFERENCES, k=min(N_CONFERENCES, len(CONFERENCES)))
    conf_ids = insert_returning_ids(
        cur,
        "INSERT INTO Conference (name, ranking) VALUES %s RETURNING confID",
        confs,
    )

    # --- Papers ------------------------------------------------------------
    papers = []
    for _ in range(N_PAPERS):
        title = random_title()
        papers.append((title, random_abstract(title)))
    paper_ids = insert_returning_ids(
        cur,
        "INSERT INTO Paper (title, abstract) VALUES %s RETURNING paperID",
        papers,
    )

    # --- Writes: every paper gets 1-5 distinct authors -------------------
    writes = [
        (a, p)
        for p in paper_ids
        for a in random.sample(author_ids, k=random.randint(1, 5))
    ]
    execute_values(cur, "INSERT INTO Writes (authorID, paperID) VALUES %s", writes)

    # --- Submits: each paper submitted to 1-3 conferences ----------------
    # Earlier submissions were rejected, the last one is accepted/rejected/pending.
    submits = []
    for p in paper_ids:
        targets = random.sample(conf_ids, k=random.randint(1, 3))
        d = random_date()
        for i, c in enumerate(targets):
            is_last = i == len(targets) - 1
            accepted = random.choice([True, True, False, None]) if is_last else False
            submits.append((p, c, accepted, d))
            d += timedelta(days=random.randint(60, 200))
    execute_values(
        cur,
        "INSERT INTO Submits (paperID, confID, isAccepted, date) VALUES %s",
        submits,
    )

    # --- Cites: each paper cites 0-8 other papers (no self-citations) ----
    cites = []
    for p in paper_ids:
        others = [q for q in paper_ids if q != p]
        for q in random.sample(others, k=random.randint(0, 8)):
            cites.append((p, q))
    execute_values(cur, "INSERT INTO Cites (paperIDfrom, paperIDto) VALUES %s", cites)

    print(
        f"Inserted {len(author_ids)} authors, {len(conf_ids)} conferences, "
        f"{len(paper_ids)} papers, {len(writes)} writes, "
        f"{len(submits)} submissions, {len(cites)} citations."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducible data")
    args = parser.parse_args()
    random.seed(args.seed)

    # `with conn` commits on success and rolls back on any exception.
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            populate(cur)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
