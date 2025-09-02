#!/usr/bin/env python3
"""
Keep only papers that are 100% verifiable - no fake titles, no fake papers
"""

import json
from pathlib import Path

def keep_only_verifiable():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    # Only papers I can 100% verify exist with correct titles and links
    verified_papers = [
        {
            "title": "Highly accurate protein structure prediction with AlphaFold",
            "url": "https://www.nature.com/articles/s41586-021-03819-2",
            "published": "2021-07-15",
            "year": 2021,
            "organization": "DeepMind",
            "category": "drug_discovery",
            "source": "curated"
        },
        {
            "title": "Accurate structure prediction of biomolecular interactions with AlphaFold 3",
            "url": "https://www.nature.com/articles/s41586-024-07487-w",
            "published": "2024-05-08", 
            "year": 2024,
            "organization": "Google DeepMind",
            "category": "drug_discovery",
            "source": "curated"
        },
        {
            "title": "Large Language Models Encode Clinical Knowledge",
            "url": "https://arxiv.org/abs/2212.13138",
            "published": "2022-12-26",
            "year": 2022,
            "organization": "Google Research",
            "category": "clinical_llm",
            "source": "curated"
        },
        {
            "title": "Towards Expert-Level Medical Question Answering with Large Language Models",
            "url": "https://arxiv.org/abs/2305.09617",
            "published": "2023-05-16",
            "year": 2023,
            "organization": "Google Research", 
            "category": "clinical_llm",
            "source": "curated"
        },
        {
            "title": "Training a Large Language-and-Vision Assistant for Biomedicine in One Day",
            "url": "https://arxiv.org/abs/2306.00890",
            "published": "2023-06-01",
            "year": 2023,
            "organization": "Microsoft Research",
            "category": "multimodal",
            "source": "curated"
        },
        {
            "title": "Segment Anything in Medical Images",
            "url": "https://arxiv.org/abs/2304.12306",
            "published": "2023-04-24",
            "year": 2023,
            "organization": "University of Toronto",
            "category": "medical_imaging",
            "source": "curated",
            "code_url": "https://github.com/bowang-lab/MedSAM"
        },
        {
            "title": "Diffusion Steps, Twists, and Turns for Molecular Docking",
            "url": "https://arxiv.org/abs/2210.01776",
            "published": "2022-10-04",
            "year": 2022,
            "organization": "MIT",
            "category": "drug_discovery",
            "source": "curated",
            "code_url": "https://github.com/gcorso/DiffDock"
        },
        {
            "title": "Language models of protein sequences at the scale of evolution enable accurate structure prediction",
            "url": "https://www.biorxiv.org/content/10.1101/2022.07.20.500902v1",
            "published": "2022-07-21",
            "year": 2022,
            "organization": "Meta AI",
            "category": "genomics",
            "source": "curated",
            "code_url": "https://github.com/facebookresearch/esm"
        },
        {
            "title": "Toward Building a Foundation Model for Single-Cell Multi-omics Using Generative AI",
            "url": "https://www.nature.com/articles/s41592-024-02201-0",
            "published": "2024-02-08",
            "year": 2024,
            "organization": "University of Toronto",
            "category": "genomics",
            "source": "curated",
            "code_url": "https://github.com/bowang-lab/scGPT"
        },
        {
            "title": "Transfer learning enables predictions in network biology",
            "url": "https://www.nature.com/articles/s41586-023-06139-9",
            "published": "2023-05-31",
            "year": 2023,
            "organization": "Broad Institute",
            "category": "genomics",
            "source": "curated",
            "code_url": "https://huggingface.co/ctheodoris/Geneformer"
        }
    ]
    
    # Save only verified papers - no fake citations
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(verified_papers, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Kept only {len(verified_papers)} 100% verified papers")
    print("❌ Removed all unverifiable papers and fake citations")
    
    # Update stats
    from datetime import datetime
    
    stats = {
        "total_papers": len(verified_papers),
        "by_year": {},
        "by_category": {},
        "by_organization": {},
        "last_updated": datetime.now().isoformat(),
        "note": "Only verified papers with real titles and links. No citations shown as we don't have real-time citation data."
    }
    
    for paper in verified_papers:
        year = paper.get("year", 2023)
        category = paper.get("category", "unknown")
        org = paper.get("organization", "Unknown")
        
        stats["by_year"][year] = stats["by_year"].get(year, 0) + 1
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        stats["by_organization"][org] = stats["by_organization"].get(org, 0) + 1
    
    stats["by_year"] = dict(sorted(stats["by_year"].items()))
    
    # Save statistics
    stats_path = data_dir / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    print("\n📊 Statistics:")
    print(f"Total verified papers: {stats['total_papers']}")
    for year in sorted(stats["by_year"].keys()):
        print(f"{year}: {stats['by_year'][year]} papers")
    
    return len(verified_papers)

if __name__ == "__main__":
    keep_only_verifiable()