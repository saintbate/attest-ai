"""Targeted arxiv search for Attest-relevant research."""
import time
from datetime import datetime, timezone
from dataclasses import dataclass
import httpx
import feedparser
import json
from pathlib import Path

ARXIV_API = "https://export.arxiv.org/api/query"


@dataclass
class Paper:
    track: str
    arxiv_id: str
    title: str
    authors: list[str]
    abstract: str
    url: str
    published: str
    categories: list[str]


TRACKS = {
    "drift_detection": [
        'abs:"concept drift detection" AND (abs:"deep learning" OR abs:"neural network")',
        'abs:"covariate shift" AND abs:"detection"',
        'abs:"maximum mean discrepancy" AND abs:"drift"',
        'abs:"distribution shift" AND abs:"computer vision"',
    ],
    "calibration_uncertainty": [
        'abs:"conformal prediction" AND abs:"deep learning"',
        'abs:"calibration" AND abs:"neural network" AND abs:"confidence"',
        'abs:"uncertainty quantification" AND abs:"regulatory"',
        'abs:"temperature scaling" AND abs:"calibration"',
    ],
    "ml_documentation": [
        'abs:"model card" AND abs:"automated"',
        'abs:"datasheet" AND abs:"dataset" AND abs:"machine learning"',
        'abs:"automated documentation" AND abs:"machine learning"',
        'abs:"FactSheets" AND abs:"AI"',
    ],
    "ai_auditing": [
        'abs:"AI audit" AND abs:"machine learning"',
        'abs:"conformity assessment" AND abs:"AI"',
        'abs:"AI Act" OR abs:"EU AI Act"',
        'abs:"algorithmic audit" AND abs:"deep learning"',
    ],
    "post_market_monitoring": [
        'abs:"production machine learning" AND abs:"monitoring"',
        'abs:"ML observability"',
        'abs:"performance degradation" AND abs:"deployment" AND abs:"machine learning"',
        'abs:"fairness drift" OR abs:"fairness monitoring"',
    ],
    "adversarial_robustness": [
        'abs:"adversarial robustness" AND abs:"object detection"',
        'abs:"robustness testing" AND abs:"computer vision"',
        'abs:"robustness certification" AND abs:"neural network"',
        'abs:"physical adversarial" AND abs:"detection"',
    ],
}


def search(query: str, max_results: int = 15) -> list[dict]:
    """Query arxiv API."""
    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }
    r = httpx.get(ARXIV_API, params=params, timeout=30)
    r.raise_for_status()
    feed = feedparser.parse(r.text)
    return feed.entries


def parse_entry(entry, track: str) -> Paper | None:
    try:
        arxiv_id = entry.id.split("/abs/")[-1].split("v")[0]
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if published.year < 2024:
            return None
        authors = [a.name for a in entry.get("authors", [])][:5]
        categories = [t.term for t in entry.get("tags", [])]
        return Paper(
            track=track,
            arxiv_id=arxiv_id,
            title=entry.title.replace("\n", " ").strip(),
            authors=authors,
            abstract=entry.summary.replace("\n", " ").strip(),
            url=entry.link,
            published=published.isoformat(),
            categories=categories,
        )
    except Exception as e:
        print(f"  parse error: {e}")
        return None


def main():
    all_papers: dict[str, list[Paper]] = {}
    seen_ids: set[str] = set()

    for track, queries in TRACKS.items():
        print(f"\n=== {track} ===")
        papers: list[Paper] = []
        for q in queries:
            print(f"  query: {q[:70]}…")
            try:
                entries = search(q, max_results=12)
            except Exception as e:
                print(f"    error: {e}")
                continue
            for e in entries:
                p = parse_entry(e, track)
                if p and p.arxiv_id not in seen_ids:
                    seen_ids.add(p.arxiv_id)
                    papers.append(p)
            time.sleep(3)  # be polite
        all_papers[track] = papers
        print(f"  → {len(papers)} papers (post-2024, deduped)")

    output = {
        track: [
            {
                "arxiv_id": p.arxiv_id,
                "title": p.title,
                "authors": p.authors,
                "abstract": p.abstract,
                "url": p.url,
                "published": p.published,
                "categories": p.categories,
            }
            for p in papers
        ]
        for track, papers in all_papers.items()
    }

    out_path = Path(__file__).parent / "results.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\n✓ wrote {out_path}")
    print(f"  total: {sum(len(v) for v in all_papers.values())} papers across {len(all_papers)} tracks")


if __name__ == "__main__":
    main()
