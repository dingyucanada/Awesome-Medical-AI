#!/usr/bin/env python3
"""
Remove papers with incorrect or non-verifiable links
"""

import json
from pathlib import Path

def remove_incorrect_papers():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    # Load existing papers
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    print(f"Starting with {len(papers)} papers")
    
    # List of papers to remove (titles that have incorrect links or are unverifiable)
    papers_to_remove = [
        # Surgical Robotics papers with issues
        "Autonomous robotic surgery: Has the future arrived?",
        "Surgical robotics: Reviewing the past, analysing the present, imagining the future",
        "Da Vinci SP robotic approach to colorectal surgery: two specific indications and short-term results",
        "Internet of Medical Things (IoMT) for orthopaedic in COVID-19 pandemic: Roles, challenges, and applications",
        
        # Telemedicine papers with issues
        "Virtual care for improved global surgical care: a perspective from the COVID-19 pandemic",
        "A systematic review of artificial intelligence and machine learning applications to wearable sensors for COVID-19",
        "Detection of COVID-19 from smartphone-recorded coughs using artificial intelligence",
        "Effectiveness of telemedicine: A systematic review of reviews",
        
        # Digital Therapeutics papers with issues
        "Digital Therapeutics for Mental Health and Addiction: The State of the Science and Vision for the Future",
        "Digital therapeutics: an integral component of digital innovation in drug development",
        "Digital therapeutic care apps with decision-support interventions improve outcomes for type 2 diabetes",
        "Prescription digital therapeutics: A review of the current landscape and future directions",
        
        # Other papers mentioned with issues
        "Visual Question Answering in the Medical Domain",
        "Machine learning for public health surveillance"  # Already fixed but double check
    ]
    
    # Remove papers
    original_count = len(papers)
    papers = [p for p in papers if p.get("title") not in papers_to_remove]
    removed_count = original_count - len(papers)
    
    print(f"❌ Removed {removed_count} papers with incorrect/unverifiable links")
    
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
        "note": "Removed papers with incorrect or unverifiable links"
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
    
    # Print category distribution
    print("\n📊 Updated category distribution:")
    for cat, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} papers")
    
    # Save statistics
    stats_path = data_dir / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    return len(papers)

if __name__ == "__main__":
    remove_incorrect_papers()