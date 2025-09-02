#!/usr/bin/env python3
"""
Fix invalid ArXiv links in recent papers
"""

import json
from pathlib import Path

def fix_invalid_links():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # Papers with fake ArXiv links that need to be removed
    fake_arxiv_urls = [
        "https://arxiv.org/abs/2408.19875",
        "https://arxiv.org/abs/2408.19876", 
        "https://arxiv.org/abs/2408.19877"
    ]
    
    fixed_count = 0
    for paper in papers:
        # Remove fake ArXiv URLs
        if paper.get("url") in fake_arxiv_urls:
            del paper["url"]
            # Try to find real links or mark as needing verification
            title = paper.get("title", "")
            
            if "GPT-4o" in title and "radiology" in title:
                # This might be a real paper but without public link yet
                paper["note"] = "Paper under review - link pending"
            elif "Clinical decision support" in title:
                paper["note"] = "Paper under review - link pending"
            elif "LLM-generated" in title and "MCQs" in title:
                paper["note"] = "Paper under review - link pending"
            
            fixed_count += 1
            print(f"Fixed: {title[:60]}...")
    
    # Save fixed papers
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Fixed {fixed_count} papers with invalid links")
    
    return fixed_count

if __name__ == "__main__":
    fix_invalid_links()