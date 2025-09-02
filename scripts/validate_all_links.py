#!/usr/bin/env python3
"""
Validate all links in the paper collection
"""

import json
import requests
from pathlib import Path
import time
from urllib.parse import urlparse

def validate_links():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    print(f"Validating {len(papers)} papers...")
    
    invalid_papers = []
    valid_count = 0
    no_link_count = 0
    
    for i, paper in enumerate(papers):
        title = paper.get("title", "")
        url = paper.get("url", "")
        
        if not url:
            no_link_count += 1
            print(f"[{i+1}/{len(papers)}] No URL: {title[:60]}...")
            continue
        
        # Parse URL
        parsed = urlparse(url)
        
        # Check for known problematic domains
        problematic_domains = [
            "inflection.ai",
            "babylonhealth.com", 
            "ada.com",
            "wysa.io"
        ]
        
        if any(domain in parsed.netloc for domain in problematic_domains):
            invalid_papers.append({
                "index": i,
                "title": title,
                "url": url,
                "reason": "Known dead domain"
            })
            print(f"[{i+1}/{len(papers)}] ❌ Dead domain: {title[:50]}...")
            continue
        
        # Check ArXiv links
        if "arxiv.org" in url:
            arxiv_id = url.split("/")[-1]
            # Check if it's a valid format
            if not arxiv_id or len(arxiv_id) < 9:
                invalid_papers.append({
                    "index": i,
                    "title": title,
                    "url": url,
                    "reason": "Invalid ArXiv ID format"
                })
                print(f"[{i+1}/{len(papers)}] ❌ Invalid ArXiv: {title[:50]}...")
                continue
            
            # ArXiv IDs after 2408.20000 are suspicious for August 2024
            if arxiv_id.startswith("2408.") and int(arxiv_id.split(".")[1]) > 20000:
                invalid_papers.append({
                    "index": i,
                    "title": title,
                    "url": url,
                    "reason": "Suspicious ArXiv ID (too high)"
                })
                print(f"[{i+1}/{len(papers)}] ❌ Suspicious ArXiv: {title[:50]}...")
                continue
        
        # Check PubMed links
        if "pubmed.ncbi.nlm.nih.gov" in url:
            pmid = url.split("/")[-1].replace("/", "")
            if not pmid.isdigit():
                invalid_papers.append({
                    "index": i,
                    "title": title,
                    "url": url,
                    "reason": "Invalid PMID format"
                })
                print(f"[{i+1}/{len(papers)}] ❌ Invalid PubMed: {title[:50]}...")
                continue
        
        # Check for fake product page patterns
        fake_patterns = [
            "/ai-research$",
            "/medical-ai$",
            "/research-2024$",
            "/research-2025$",
            "/einstein-gpt",
            "/pi-health",
            "/generative-ai-triage"
        ]
        
        if any(pattern in url.lower() for pattern in fake_patterns):
            invalid_papers.append({
                "index": i,
                "title": title,
                "url": url,
                "reason": "Suspicious product page URL"
            })
            print(f"[{i+1}/{len(papers)}] ❌ Fake product page: {title[:50]}...")
            continue
        
        valid_count += 1
        print(f"[{i+1}/{len(papers)}] ✓ Valid format: {title[:50]}...")
    
    print(f"\n" + "="*70)
    print(f"Validation Results:")
    print(f"  Total papers: {len(papers)}")
    print(f"  Valid URLs: {valid_count}")
    print(f"  No URL: {no_link_count}")
    print(f"  Invalid/Suspicious: {len(invalid_papers)}")
    
    if invalid_papers:
        print(f"\n❌ Papers to remove ({len(invalid_papers)}):")
        for inv in invalid_papers:
            print(f"  [{inv['index']}] {inv['title'][:60]}...")
            print(f"      URL: {inv['url']}")
            print(f"      Reason: {inv['reason']}")
        
        # Remove invalid papers
        print("\nRemoving invalid papers...")
        indices_to_remove = sorted([p["index"] for p in invalid_papers], reverse=True)
        for idx in indices_to_remove:
            del papers[idx]
        
        # Save cleaned papers
        with open(papers_path, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Removed {len(invalid_papers)} invalid papers")
        print(f"📊 Papers remaining: {len(papers)}")
        
        # Update stats
        from datetime import datetime
        
        stats = {
            "total_papers": len(papers),
            "classic_papers": len([p for p in papers if p.get("is_classic")]),
            "recent_papers": len([p for p in papers if not p.get("is_classic")]),
            "papers_2024": len([p for p in papers if p.get("year") == 2024]),
            "papers_2025": len([p for p in papers if p.get("year") == 2025]),
            "by_source": {},
            "by_category": {},
            "by_year": {},
            "by_organization": {},
            "last_updated": datetime.now().isoformat()
        }
        
        for paper in papers:
            source = paper.get("source", "unknown")
            category = paper.get("category", "unknown")
            year = paper.get("year", 2024)
            org = paper.get("organization", "Unknown")
            
            stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            stats["by_year"][year] = stats["by_year"].get(year, 0) + 1
            stats["by_organization"][org] = stats["by_organization"].get(org, 0) + 1
        
        stats["by_year"] = dict(sorted(stats["by_year"].items()))
        
        # Save statistics
        stats_path = data_dir / "stats.json"
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
    else:
        print("\n✅ No invalid papers found!")
    
    return len(invalid_papers)

if __name__ == "__main__":
    validate_links()