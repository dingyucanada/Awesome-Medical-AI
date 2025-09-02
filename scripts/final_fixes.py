#!/usr/bin/env python3
"""
Final fixes for incorrect paper links
"""

import json
from pathlib import Path

def final_fixes():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    # Load existing papers
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # Find and fix the Machine learning for public health surveillance paper
    for paper in papers:
        if paper.get("title") == "Machine learning for public health surveillance":
            print(f"✅ Found paper: {paper['title']}")
            # This paper appears to be from a journal, update the URL
            paper["url"] = "https://www.sciencedirect.com/science/article/pii/S1532046421002847"
            print(f"   Fixed URL to: {paper['url']}")
    
    # Sort by date (newest first)
    papers.sort(key=lambda x: x.get("published", "2020-01-01"), reverse=True)
    
    # Save updated collection
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Total papers: {len(papers)}")
    
    return len(papers)

if __name__ == "__main__":
    final_fixes()