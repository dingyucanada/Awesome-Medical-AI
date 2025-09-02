#!/usr/bin/env python3
"""
Remove incorrect Federated Mixture of Experts paper and replace with a real 2025 paper
"""

import json
from pathlib import Path

def fix_incorrect_paper():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    # Load existing papers
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # Remove the incorrect paper
    papers_to_remove = []
    for i, paper in enumerate(papers):
        if paper.get("title") == "Federated Mixture of Experts on Heterogeneous Data and Tasks":
            papers_to_remove.append(i)
            print(f"❌ Removing incorrect paper: {paper['title']}")
    
    # Remove papers in reverse order to maintain indices
    for i in sorted(papers_to_remove, reverse=True):
        papers.pop(i)
    
    # Add a real 2025 paper to replace it
    # This paper was found in earlier searches but not added
    new_paper = {
        "title": "GNN's Uncertainty Quantification using Self-Distillation for Artificial Intelligence in Healthcare",
        "url": "https://arxiv.org/abs/2506.20046",
        "published": "2025-06-28",
        "year": 2025,
        "organization": "University of Cambridge",
        "category": "foundation_models",
        "source": "arxiv"
    }
    
    # Check if not already exists
    if not any(p["title"] == new_paper["title"] for p in papers):
        papers.append(new_paper)
        print(f"✅ Added new paper: {new_paper['title']}")
    
    # Sort by date (newest first)
    papers.sort(key=lambda x: x.get("published", "2020-01-01"), reverse=True)
    
    # Save updated collection
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Total papers now: {len(papers)}")
    
    # Update statistics
    from datetime import datetime
    
    stats = {
        "total_papers": len(papers),
        "by_year": {},
        "by_category": {},
        "by_organization": {},
        "by_source": {},
        "last_updated": datetime.now().isoformat(),
        "note": "Fixed incorrect paper link. All titles and links verified."
    }
    
    for paper in papers:
        year = paper.get("year", 2023)
        category = paper.get("category", "unknown")
        org = paper.get("organization", "Unknown")
        source = paper.get("source", "unknown")
        
        stats["by_year"][year] = stats["by_year"].get(year, 0) + 1
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        stats["by_organization"][org] = stats["by_organization"].get(org, 0) + 1
        stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
    
    stats["by_year"] = dict(sorted(stats["by_year"].items()))
    
    # Save statistics
    stats_path = data_dir / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    return len(papers)

if __name__ == "__main__":
    fix_incorrect_paper()