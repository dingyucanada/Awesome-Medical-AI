#!/usr/bin/env python3
"""
Remove papers with incorrect/mismatched links and dead company pages
"""

import json
from pathlib import Path

def remove_problematic_papers():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # Papers to remove (mismatched content or dead links)
    titles_to_remove = [
        # Mismatched PubMed links
        "Visual art and representation in cardiology: Past, present, and future.",
        "Analyses of different prescriptions for health using artificial intelligence: a critical approach based on the internal epistemology of AI",
        "Clinical decision support for pharmacologic management of treatment-resistant depression with augmented large language models.",
        
        # Dead company product pages
        "Pi Health: Personal AI for Mental Health Support",
        "Babylon Health's Generative AI Triage System",
        "Ada Health: LLM-Enhanced Symptom Assessment",
        "Salesforce Health Cloud Einstein GPT",
        "Wysa 2.0: Evolution of an AI Mental Health Companion",
        
        # Other problematic entries that were fake
        "Evaluation of GPT-4o for multilingual translation of radiology reports across imaging modalities.",
        "Assessing LLM-generated vs. expert-created clinical anatomy MCQs: a student perception-based comparative study in medical education.",
        
        # These fake URLs should be removed
        "SafeHealth: Constitutional AI for Medical Applications",
        "MedAgent: Multi-Agent System for Clinical Decision Support",
        "AutoMed: Autonomous Medical AI Agents with Tool Use",
        "HospitalGPT: Agent-Based Simulation of Hospital Operations",
        "MedFlow: Orchestrating Medical AI Workflows with Apache Airflow",
        "MedPrompt: Prompt Engineering for Clinical Applications",
        "Chain-of-Diagnosis: Reasoning Chains for Medical AI",
        "TinyMed: Compressed Medical LLMs for Edge Deployment",
        "EdgeHealth: On-Device Medical AI with 2B Parameters",
        "HealthKube: Kubernetes for Medical AI Deployment",
        "MedMLOps: MLOps for Medical AI Systems",
        "HealthTrace: Distributed Tracing for Medical AI Systems",
        "AutoHealth: AutoML for Medical AI Development",
        "H2O-Health: AutoML Platform for Clinical Predictions"
    ]
    
    # URLs that are known to be fake or dead
    problematic_urls = [
        "https://inflection.ai/pi-health",
        "https://www.babylonhealth.com/ai-research",
        "https://ada.com/medical-ai",
        "https://www.salesforce.com/products/health-cloud/einstein-gpt/",
        "https://www.wysa.io/research-2024"
    ]
    
    original_count = len(papers)
    
    # Filter out problematic papers
    cleaned_papers = []
    removed_count = 0
    
    for paper in papers:
        title = paper.get("title", "")
        url = paper.get("url", "")
        
        # Check if paper should be removed
        should_remove = False
        
        # Check by title
        if title in titles_to_remove:
            should_remove = True
            print(f"Removing by title: {title[:60]}...")
        
        # Check by URL
        elif url in problematic_urls:
            should_remove = True
            print(f"Removing by URL: {title[:60]}... ({url})")
        
        # Check for other indicators of fake papers
        elif paper.get("note") == "Paper under review - link pending":
            should_remove = True
            print(f"Removing pending paper: {title[:60]}...")
        
        if not should_remove:
            cleaned_papers.append(paper)
        else:
            removed_count += 1
    
    # Save cleaned papers
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_papers, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Removed {removed_count} problematic papers")
    print(f"📊 Papers remaining: {len(cleaned_papers)} (was {original_count})")
    
    # Update stats
    from datetime import datetime
    
    stats = {
        "total_papers": len(cleaned_papers),
        "classic_papers": len([p for p in cleaned_papers if p.get("is_classic")]),
        "recent_papers": len([p for p in cleaned_papers if not p.get("is_classic")]),
        "papers_2024": len([p for p in cleaned_papers if p.get("year") == 2024]),
        "papers_2025": len([p for p in cleaned_papers if p.get("year") == 2025]),
        "by_source": {},
        "by_category": {},
        "by_year": {},
        "by_organization": {},
        "last_updated": datetime.now().isoformat()
    }
    
    for paper in cleaned_papers:
        source = paper.get("source", "unknown")
        category = paper.get("category", "unknown")
        year = paper.get("year", int(paper.get("published", "2023")[:4]) if paper.get("published") else 2023)
        org = paper.get("organization", "Unknown")
        
        stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        stats["by_year"][year] = stats["by_year"].get(year, 0) + 1
        stats["by_organization"][org] = stats["by_organization"].get(org, 0) + 1
    
    # Sort year dict
    stats["by_year"] = dict(sorted(stats["by_year"].items()))
    
    # Save statistics
    stats_path = data_dir / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    print("\n📊 Updated Statistics:")
    print(f"Total: {stats['total_papers']}")
    print(f"2024 papers: {stats['papers_2024']}")
    print(f"2025 papers: {stats['papers_2025']}")
    
    return removed_count

if __name__ == "__main__":
    remove_problematic_papers()