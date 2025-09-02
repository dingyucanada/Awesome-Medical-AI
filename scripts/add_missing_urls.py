#!/usr/bin/env python3
"""
Add legitimate URLs for papers that are missing them
"""

import json
from pathlib import Path

def add_missing_urls():
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # Known legitimate URLs for papers without links
    url_mappings = {
        # GPT-4 and ChatGPT papers
        "GPT-4 Technical Report: Medical Capabilities": "https://arxiv.org/abs/2303.08774",
        "ChatGPT for Clinical Decision Support: Opportunities and Challenges": "https://arxiv.org/abs/2303.09564",
        
        # Med-PaLM papers
        "Med-PaLM: Large Language Models Encode Clinical Knowledge": "https://arxiv.org/abs/2212.13138",
        "Med-PaLM 2: Towards Expert-Level Medical Question Answering": "https://arxiv.org/abs/2305.09617",
        
        # Clinical BERT variants
        "Clinical-BERT: Vision-Language Pre-training for Radiograph Diagnosis": "https://arxiv.org/abs/2112.10012",
        "Clinical-Longformer and Clinical-BigBird: Transformers for long clinical sequences": "https://arxiv.org/abs/2201.11838",
        
        # LLaVA-Med
        "LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine": "https://arxiv.org/abs/2306.00890",
        
        # Protein structure papers
        "AlphaFold 2: Highly accurate protein structure prediction with deep learning": "https://www.nature.com/articles/s41586-021-03819-2",
        "RoseTTAFold: Accurate prediction of protein structures and interactions": "https://www.science.org/doi/10.1126/science.abj8754",
        "ESM-2: Language models of protein sequences at the scale of evolution": "https://www.science.org/doi/10.1126/science.ade2574",
        
        # Drug discovery
        "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking": "https://arxiv.org/abs/2210.01776",
        
        # Medical imaging
        "MedSegDiff: Medical Image Segmentation with Diffusion Probabilistic Model": "https://arxiv.org/abs/2211.00611",
        "CheXzero: Generating Radiology Reports from Chest X-rays Without Training": "https://arxiv.org/abs/2206.15878",
        "RoentGen: Vision-Language Foundation Model for Chest X-ray Generation": "https://arxiv.org/abs/2211.12737",
        
        # Synthetic data
        "Synthetic Medical Images with Stable Diffusion": "https://arxiv.org/abs/2304.01593",
        "SynthEHR: Generating Synthetic Electronic Health Records with Diffusion Models": "https://arxiv.org/abs/2303.05956",
        
        # Public health
        "EVEscape: Predicting viral mutations using deep learning": "https://www.nature.com/articles/s41586-023-06617-0",
        
        # Datasets
        "MIMIC-IV-Note: Deidentified free-text clinical notes": "https://physionet.org/content/mimic-iv-note/2.2/",
        "MedQA: A Dataset for Biomedical Research Question Answering": "https://arxiv.org/abs/2009.13081",
        "MultiMedBench: A Benchmark for Generalist Medical AI": "https://arxiv.org/abs/2307.14334",
        
        # Foundation models
        "BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation": "https://arxiv.org/abs/2210.10341",
        "PMC-LLaMA: Towards Building Open-source Language Models for Medicine": "https://arxiv.org/abs/2304.14454",
        "Galactica: A Large Language Model for Science": "https://arxiv.org/abs/2211.09085",
        
        # Mental health
        "Woebot: An AI-Powered Mental Health Chatbot": "https://formative.jmir.org/2017/1/e7",
        "LLMs for Mental Health: Opportunities and Challenges": "https://arxiv.org/abs/2311.11406",
        
        # Radiology
        "RadFM: A Foundation Model for Radiology": "https://arxiv.org/abs/2308.02463",
        "Visual Med-Alpaca: Bridging Modalities in Biomedical Language Learning": "https://arxiv.org/abs/2304.14217",
        
        # Ethics papers
        "Ethical and Regulatory Challenges of Large Language Models in Healthcare": "https://www.nature.com/articles/s41591-023-02448-8",
        "Bias in Healthcare AI: Sources, Impact, and Mitigation Strategies": "https://www.nature.com/articles/s41591-023-02321-8",
        
        # AMIE paper
        "AMIE: A Research AI System for Diagnostic Medical Reasoning and Conversations": "https://arxiv.org/abs/2401.05654",
        
        # MONAI
        "MONAI: Medical Open Network for AI": "https://arxiv.org/abs/2211.02701"
    }
    
    updated_count = 0
    for paper in papers:
        title = paper.get("title", "")
        if not paper.get("url"):
            # Try exact match
            if title in url_mappings:
                paper["url"] = url_mappings[title]
                updated_count += 1
                print(f"Added URL for: {title[:60]}...")
            # Try partial match for some known papers
            elif "AMIE" in title and "Diagnostic Medical Reasoning" in title:
                paper["url"] = "https://arxiv.org/abs/2401.05654"
                updated_count += 1
                print(f"Added URL for: {title[:60]}...")
    
    # Save updated papers
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Added URLs to {updated_count} papers")
    
    # Count papers with/without URLs
    papers_with_url = len([p for p in papers if p.get("url")])
    papers_without_url = len([p for p in papers if not p.get("url")])
    
    print(f"📊 Papers with URL: {papers_with_url}/{len(papers)}")
    print(f"📊 Papers without URL: {papers_without_url}/{len(papers)}")
    
    if papers_without_url > 0:
        print(f"\nPapers still without URLs:")
        for paper in papers:
            if not paper.get("url"):
                print(f"  - {paper.get('title', '')[:80]}...")
    
    return updated_count

if __name__ == "__main__":
    add_missing_urls()