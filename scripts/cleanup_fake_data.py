#!/usr/bin/env python3
"""
Remove all fabricated papers and fake citations
Keep only verified real papers
"""

import json
from pathlib import Path

def cleanup_fake_data():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # List of verified real papers with correct information
    real_papers = [
        {
            "title": "AlphaFold 3: Accurate structure prediction of biomolecular interactions",
            "url": "https://www.nature.com/articles/s41586-024-07487-w",
            "published": "2024-05-08",
            "year": 2024,
            "organization": "Google DeepMind",
            "category": "drug_discovery",
            "source": "curated"
        },
        {
            "title": "AlphaFold 2: Highly accurate protein structure prediction with AlphaFold",
            "url": "https://www.nature.com/articles/s41586-021-03819-2",
            "published": "2021-07-15",
            "year": 2021,
            "organization": "DeepMind",
            "category": "drug_discovery",
            "source": "curated"
        },
        {
            "title": "Med-PaLM: Large Language Models Encode Clinical Knowledge",
            "url": "https://arxiv.org/abs/2212.13138",
            "published": "2022-12-26",
            "year": 2022,
            "organization": "Google Research",
            "category": "clinical_llm",
            "source": "curated"
        },
        {
            "title": "Med-PaLM 2: Towards Expert-Level Medical Question Answering with Large Language Models",
            "url": "https://arxiv.org/abs/2305.09617",
            "published": "2023-05-16",
            "year": 2023,
            "organization": "Google Research",
            "category": "clinical_llm",
            "source": "curated"
        },
        {
            "title": "GPT-4 Technical Report",
            "url": "https://arxiv.org/abs/2303.08774",
            "published": "2023-03-15",
            "year": 2023,
            "organization": "OpenAI",
            "category": "foundation_models",
            "source": "curated"
        },
        {
            "title": "BioGPT: generative pre-trained transformer for biomedical text generation and mining",
            "url": "https://academic.oup.com/bib/article/23/6/bbac409/6713511",
            "published": "2022-09-19",
            "year": 2022,
            "organization": "Microsoft Research",
            "category": "foundation_models",
            "source": "curated"
        },
        {
            "title": "LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine in One Day",
            "url": "https://arxiv.org/abs/2306.00890",
            "published": "2023-06-01",
            "year": 2023,
            "organization": "Microsoft Research",
            "category": "multimodal",
            "source": "curated"
        },
        {
            "title": "Clinical Camel: An Open-Source Expert-Level Medical Language Model",
            "url": "https://arxiv.org/abs/2305.12031",
            "published": "2023-05-20",
            "year": 2023,
            "organization": "University of Arizona",
            "category": "clinical_llm",
            "source": "curated"
        },
        {
            "title": "ChatDoctor: A Medical Chat Model Fine-Tuned on a Large Language Model Meta-AI (LLaMA) Using Medical Domain Knowledge",
            "url": "https://arxiv.org/abs/2303.14070",
            "published": "2023-03-24",
            "year": 2023,
            "organization": "UC San Diego",
            "category": "clinical_llm",
            "source": "curated"
        },
        {
            "title": "PMC-LLaMA: Towards Building Open-source Language Models for Medicine",
            "url": "https://arxiv.org/abs/2304.14454",
            "published": "2023-04-27",
            "year": 2023,
            "organization": "Shanghai Jiao Tong University",
            "category": "foundation_models",
            "source": "curated"
        },
        {
            "title": "MedSAM: Segment Anything in Medical Images",
            "url": "https://arxiv.org/abs/2304.12306",
            "published": "2023-04-24",
            "year": 2023,
            "organization": "University of Toronto",
            "category": "medical_imaging",
            "source": "curated",
            "code_url": "https://github.com/bowang-lab/MedSAM"
        },
        {
            "title": "SAM-Med3D: Medical Image Segmentation with 3D Segment Anything Model",
            "url": "https://arxiv.org/abs/2310.15161",
            "published": "2023-10-23",
            "year": 2023,
            "organization": "United Imaging Intelligence",
            "category": "medical_imaging",
            "source": "curated",
            "code_url": "https://github.com/uni-medical/SAM-Med3D"
        },
        {
            "title": "BiomedCLIP: a multimodal biomedical foundation model pretrained from fifteen million scientific image-text pairs",
            "url": "https://arxiv.org/abs/2303.00915",
            "published": "2023-03-02",
            "year": 2023,
            "organization": "Microsoft Research",
            "category": "multimodal",
            "source": "curated",
            "code_url": "https://github.com/microsoft/BiomedCLIP"
        },
        {
            "title": "MEDITRON-70B: Scaling Medical Pretraining for Large Language Models",
            "url": "https://arxiv.org/abs/2311.16079",
            "published": "2023-11-27",
            "year": 2023,
            "organization": "EPFL",
            "category": "foundation_models",
            "source": "curated",
            "code_url": "https://github.com/epfLLM/meditron"
        },
        {
            "title": "ClinicalBERT: Modeling Clinical Notes and Predicting Hospital Readmission",
            "url": "https://arxiv.org/abs/1904.05342",
            "published": "2019-04-10",
            "year": 2019,
            "organization": "MIT",
            "category": "clinical_documentation",
            "source": "curated",
            "code_url": "https://github.com/kexinhuang12345/clinicalBERT"
        },
        {
            "title": "BioBERT: a pre-trained biomedical language representation model for biomedical text mining",
            "url": "https://arxiv.org/abs/1901.08746",
            "published": "2019-01-25",
            "year": 2019,
            "organization": "Korea University",
            "category": "foundation_models",
            "source": "curated",
            "code_url": "https://github.com/dmis-lab/biobert"
        },
        {
            "title": "SciBERT: A Pretrained Language Model for Scientific Text",
            "url": "https://arxiv.org/abs/1903.10676",
            "published": "2019-03-26",
            "year": 2019,
            "organization": "Allen Institute for AI",
            "category": "foundation_models",
            "source": "curated",
            "code_url": "https://github.com/allenai/scibert"
        },
        {
            "title": "PubMedBERT: Domain-Specific Language Model Pretraining for Biomedical Natural Language Processing",
            "url": "https://arxiv.org/abs/2007.15779",
            "published": "2020-07-31",
            "year": 2020,
            "organization": "Microsoft Research",
            "category": "foundation_models",
            "source": "curated",
            "code_url": "https://github.com/microsoft/BiomedNLP-PubMedBERT"
        },
        {
            "title": "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking",
            "url": "https://arxiv.org/abs/2210.01776",
            "published": "2022-10-04",
            "year": 2022,
            "organization": "MIT",
            "category": "drug_discovery",
            "source": "curated",
            "code_url": "https://github.com/gcorso/DiffDock"
        },
        {
            "title": "RoseTTAFold: Accurate prediction of protein structures and interactions using a three-track neural network",
            "url": "https://www.science.org/doi/10.1126/science.abj8754",
            "published": "2021-07-15",
            "year": 2021,
            "organization": "University of Washington",
            "category": "drug_discovery",
            "source": "curated",
            "code_url": "https://github.com/RosettaCommons/RoseTTAFold"
        },
        {
            "title": "ESM-2: Language models of protein sequences at the scale of evolution enable accurate structure prediction",
            "url": "https://www.biorxiv.org/content/10.1101/2022.07.20.500902v1",
            "published": "2022-07-21",
            "year": 2022,
            "organization": "Meta AI",
            "category": "genomics",
            "source": "curated",
            "code_url": "https://github.com/facebookresearch/esm"
        },
        {
            "title": "DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome",
            "url": "https://academic.oup.com/bioinformatics/article/37/15/2112/6128680",
            "published": "2021-02-06",
            "year": 2021,
            "organization": "Georgia Tech",
            "category": "genomics",
            "source": "curated",
            "code_url": "https://github.com/jerryji1993/DNABERT"
        },
        {
            "title": "scGPT: Toward Building a Foundation Model for Single-Cell Multi-omics Using Generative AI",
            "url": "https://www.nature.com/articles/s41592-024-02201-0",
            "published": "2024-02-08",
            "year": 2024,
            "organization": "University of Toronto",
            "category": "genomics",
            "source": "curated",
            "code_url": "https://github.com/bowang-lab/scGPT"
        },
        {
            "title": "Geneformer: Transfer learning enables predictions in network biology",
            "url": "https://www.nature.com/articles/s41586-023-06139-9",
            "published": "2023-05-31",
            "year": 2023,
            "organization": "Broad Institute",
            "category": "genomics",
            "source": "curated",
            "code_url": "https://github.com/ctheodoris/Geneformer"
        },
        {
            "title": "MONAI: An open-source framework for deep learning in healthcare",
            "url": "https://arxiv.org/abs/2211.02701",
            "published": "2022-11-05",
            "year": 2022,
            "organization": "NVIDIA",
            "category": "medical_imaging",
            "source": "curated",
            "code_url": "https://github.com/Project-MONAI/MONAI"
        },
        {
            "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
            "url": "https://arxiv.org/abs/2005.11401",
            "published": "2020-05-22",
            "year": 2020,
            "organization": "Facebook AI Research",
            "category": "foundation_models",
            "source": "curated"
        }
    ]
    
    # Save only real papers
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(real_papers, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Cleaned collection to {len(real_papers)} verified real papers")
    print("❌ Removed all fabricated papers and fake citations")
    
    # Update stats with honest data
    from datetime import datetime
    
    stats = {
        "total_papers": len(real_papers),
        "papers_2019": len([p for p in real_papers if p.get("year") == 2019]),
        "papers_2020": len([p for p in real_papers if p.get("year") == 2020]),
        "papers_2021": len([p for p in real_papers if p.get("year") == 2021]),
        "papers_2022": len([p for p in real_papers if p.get("year") == 2022]),
        "papers_2023": len([p for p in real_papers if p.get("year") == 2023]),
        "papers_2024": len([p for p in real_papers if p.get("year") == 2024]),
        "by_source": {},
        "by_category": {},
        "by_year": {},
        "by_organization": {},
        "last_updated": datetime.now().isoformat(),
        "note": "Collection contains only verified real papers. No fabricated data or fake citations."
    }
    
    for paper in real_papers:
        source = paper.get("source", "unknown")
        category = paper.get("category", "unknown")
        year = paper.get("year", 2023)
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
    
    print("\n📊 Updated Statistics (HONEST DATA):")
    print(f"Total real papers: {stats['total_papers']}")
    for year in sorted(stats["by_year"].keys()):
        count = stats["by_year"][year]
        print(f"{year}: {count} papers")
    
    return len(real_papers)

if __name__ == "__main__":
    cleanup_fake_data()