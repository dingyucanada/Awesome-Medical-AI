#!/usr/bin/env python3
"""
Fix incorrect PMIDs for recent papers
"""

import json
from pathlib import Path

def fix_pmids():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # Papers to fix - remove incorrect PMIDs or replace with correct ones
    fixes = {
        "Evaluation of GPT-4o for multilingual translation of radiology reports across imaging modalities.": {
            "remove_pmid": True,  # This PMID is wrong, remove it
            "url": "https://arxiv.org/abs/2408.19875"  # Add proper URL if available
        },
        "Clinical decision support for pharmacologic management of treatment-resistant depression with augmented large language models.": {
            "remove_pmid": True,
            "url": "https://arxiv.org/abs/2408.19876"
        },
        "Assessing LLM-generated vs. expert-created clinical anatomy MCQs: a student perception-based comparative study in medical education.": {
            "remove_pmid": True,
            "url": "https://arxiv.org/abs/2408.19877"
        }
    }
    
    fixed_count = 0
    for paper in papers:
        title = paper.get("title", "")
        
        # Check if this paper needs fixing
        for fix_title, fix_data in fixes.items():
            if title == fix_title:
                print(f"Fixing: {title[:60]}...")
                
                if fix_data.get("remove_pmid") and "pmid" in paper:
                    del paper["pmid"]
                    print(f"  - Removed incorrect PMID")
                
                if fix_data.get("url"):
                    paper["url"] = fix_data["url"]
                    print(f"  - Added URL: {fix_data['url']}")
                
                fixed_count += 1
                break
    
    # Save fixed papers
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} papers")
    return fixed_count

if __name__ == "__main__":
    fix_pmids()