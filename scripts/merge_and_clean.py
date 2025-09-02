#!/usr/bin/env python3
"""
Merge classic papers with current collection and clean up non-healthcare papers
"""

import json
from pathlib import Path
from datetime import datetime

def is_healthcare_related(paper):
    """Check if a paper is healthcare related"""
    non_healthcare_keywords = [
        "gravitational wave", "entropy cone", "hartree equation",
        "quantum", "tsirelson", "fair allocation", "recommendation model"
    ]
    
    healthcare_keywords = [
        "medical", "clinical", "health", "patient", "drug", "disease",
        "therapy", "diagnosis", "treatment", "biomedical", "hospital",
        "doctor", "nurse", "radiology", "surgery", "pharmaceutical"
    ]
    
    title = paper.get("title", "").lower()
    abstract = paper.get("abstract", "").lower()
    text = title + " " + abstract
    
    # Check for non-healthcare keywords
    for keyword in non_healthcare_keywords:
        if keyword in text:
            return False
    
    # Check for healthcare keywords
    for keyword in healthcare_keywords:
        if keyword in text:
            return True
    
    # Check category
    if paper.get("category") in ["medical_imaging", "clinical_apps", "patient_care", 
                                  "drug_discovery", "documentation", "genomics", "ethics"]:
        return True
    
    return False

def merge_collections():
    """Merge classic and current papers, remove non-healthcare"""
    data_dir = Path(__file__).parent.parent / "data"
    
    # Load current papers
    current_path = data_dir / "papers_latest.json"
    with open(current_path, "r", encoding="utf-8") as f:
        current_papers = json.load(f)
    
    # Load classic papers
    classic_path = data_dir / "comprehensive_papers.json"
    with open(classic_path, "r", encoding="utf-8") as f:
        classic_papers = json.load(f)
    
    print(f"Original current papers: {len(current_papers)}")
    
    # Filter out non-healthcare papers from current collection
    healthcare_current = [p for p in current_papers if is_healthcare_related(p)]
    removed = len(current_papers) - len(healthcare_current)
    print(f"Removed {removed} non-healthcare papers from current collection")
    
    # Papers to remove (non-healthcare)
    non_healthcare_titles = [
        "A new characterization of the holographic entropy cone",
        "Scattering for the non-radial inhomogeneous Hartree equation with a potential",
        "An Introduction to Gravitational Wave Theory",
        "Unitary induced channels and Tsirelson's problem",
        "Sequential Fair Allocation With Replenishments",
        "DMGIN: How Multimodal LLMs Enhance Large Recommendation Models"
    ]
    
    healthcare_current = [p for p in healthcare_current 
                         if p.get("title", "").split(":")[0] not in non_healthcare_titles]
    
    print(f"Healthcare papers from current: {len(healthcare_current)}")
    print(f"Classic papers to add: {len(classic_papers)}")
    
    # Update categories for current papers
    category_mapping = {
        "foundation": "foundation_models",
        "medical_imaging": "medical_imaging",
        "clinical_apps": "clinical_llm",
        "patient_care": "patient_interaction",
        "drug_discovery": "drug_discovery",
        "documentation": "clinical_documentation",
        "genomics": "genomics",
        "ethics": "ethics_fairness"
    }
    
    for paper in healthcare_current:
        old_cat = paper.get("category", "")
        paper["category"] = category_mapping.get(old_cat, old_cat)
    
    # Combine all papers
    all_papers = classic_papers + healthcare_current
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_papers = []
    for paper in all_papers:
        title = paper.get("title", "").lower()[:50]
        if title not in seen_titles:
            seen_titles.add(title)
            unique_papers.append(paper)
    
    # Sort by year (desc) then citations (desc)
    unique_papers.sort(key=lambda x: (
        x.get("year", int(x.get("published", "2023")[:4])),
        x.get("citations", 0)
    ), reverse=True)
    
    print(f"\nFinal collection: {len(unique_papers)} papers")
    
    # Save merged collection
    output_path = data_dir / "papers_latest.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_papers, f, indent=2, ensure_ascii=False)
    
    # Update statistics
    stats = {
        "total_papers": len(unique_papers),
        "classic_papers": len([p for p in unique_papers if p.get("is_classic")]),
        "recent_papers": len([p for p in unique_papers if not p.get("is_classic")]),
        "by_source": {},
        "by_category": {},
        "by_year": {},
        "by_organization": {},
        "last_updated": datetime.now().isoformat()
    }
    
    for paper in unique_papers:
        source = paper.get("source", "unknown")
        category = paper.get("category", "unknown")
        year = paper.get("year", int(paper.get("published", "2023")[:4]))
        org = paper.get("organization", "Unknown")
        
        stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        stats["by_year"][year] = stats["by_year"].get(year, 0) + 1
        stats["by_organization"][org] = stats["by_organization"].get(org, 0) + 1
    
    # Save statistics
    stats_path = data_dir / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    print("\n📊 Final Statistics:")
    print(f"Total: {stats['total_papers']}")
    print(f"Classic (2020-2024): {stats['classic_papers']}")
    print(f"Recent (2025): {stats['recent_papers']}")
    
    print("\nBy Category:")
    for cat, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    
    print("\nBy Year:")
    for year, count in sorted(stats["by_year"].items()):
        print(f"  {year}: {count}")
    
    print("\nTop Organizations:")
    for org, count in sorted(stats["by_organization"].items(), key=lambda x: x[1], reverse=True)[:10]:
        if count > 1:
            print(f"  {org}: {count}")

if __name__ == "__main__":
    merge_collections()