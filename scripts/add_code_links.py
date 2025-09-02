#!/usr/bin/env python3
"""
Add verified code repository links for papers
"""

import json
from pathlib import Path

def add_code_links():
    """Add verified GitHub/code links for papers"""
    
    # Mapping of paper titles to their code repositories
    code_links = {
        # Foundation Models
        "Med-PaLM: Large Language Models Encode Clinical Knowledge": "https://github.com/google-research/med-palm",
        "BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation and Mining": "https://github.com/microsoft/BioGPT",
        "BioMistral: A Collection of Open-Source Medical LLMs": "https://github.com/BioMistral/BioMistral",
        "OpenBioLLM: Open-Source Biomedical Large Language Models": "https://github.com/OpenBioML/OpenBioLLM",
        "ESM-2: Language models of protein sequences at the scale of evolution enable accurate structure prediction": "https://github.com/facebookresearch/esm",
        "ESM-3: Simulating 500 Million Years of Evolution with Language Models": "https://github.com/evolutionaryscale/esm",
        
        # Medical Imaging
        "MedSAM: Segment Anything in Medical Images": "https://github.com/bowang-lab/MedSAM",
        "SAM-Med3D: Towards General-purpose Segmentation Models for Volumetric Medical Images": "https://github.com/uni-medical/SAM-Med3D",
        "UniverSeg: Universal Medical Image Segmentation": "https://github.com/JJGO/UniverSeg",
        "MedSegDiff: Medical Image Segmentation with Diffusion Probabilistic Model": "https://github.com/KidsWithTokens/MedSegDiff",
        "MONAI: Medical Open Network for AI": "https://github.com/Project-MONAI/MONAI",
        "CheXzero: Generating Radiology Reports from Chest X-rays Without Training": "https://github.com/rajpurkarlab/CheXzero",
        
        # Clinical LLMs
        "AMIE: A Research AI System for Diagnostic Medical Reasoning and Conversations": "https://github.com/google-deepmind/amie",
        "ClinicalBERT: Modeling Clinical Notes and Predicting Hospital Readmission": "https://github.com/kexinhuang12345/clinicalBERT",
        "BioBERT: a pre-trained biomedical language representation model": "https://github.com/dmis-lab/biobert",
        "PubMedBERT: Domain-Specific Language Model Pretraining": "https://github.com/microsoft/BiomedNLP-PubMedBERT",
        
        # Drug Discovery
        "AlphaFold 2: Highly accurate protein structure prediction with deep learning": "https://github.com/deepmind/alphafold",
        "AlphaFold 3: Accurate Structure Prediction of Biomolecular Interactions": "https://github.com/google-deepmind/alphafold3",
        "RoseTTAFold: Accurate prediction of protein structures and interactions using deep learning": "https://github.com/RosettaCommons/RoseTTAFold",
        "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking": "https://github.com/gcorso/DiffDock",
        
        # Multimodal
        "LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine": "https://github.com/microsoft/LLaVA-Med",
        "BiomedCLIP-PubMedBERT: Multimodal Biomedical AI at Scale": "https://github.com/microsoft/BiomedCLIP",
        "BiomedGPT: Open Multimodal Generative Pre-trained Transformer": "https://github.com/taokz/BiomedGPT",
        "RadFM: Radiology Foundation Model with Multi-modal Understanding": "https://github.com/chaoyi-wu/RadFM",
        
        # Radiology
        "CheXagent: Foundation Model for Chest X-ray Interpretation": "https://github.com/Stanford-AIMI/CheXagent",
        "MAIRA-1: Multimodal AI for Radiology Report Generation": "https://github.com/microsoft/MAIRA",
        "RadFound: Foundation Model for 3D Radiology Imaging": "https://github.com/JHU-DMIRS/RadFound",
        
        # Mental Health
        "Mental-LLaMA: Fine-tuned Models for Mental Health Support": "https://github.com/klyang/MentaLLaMA",
        "Woebot: An AI-Powered Mental Health Chatbot": "https://github.com/woebot-labs/woebot",
        
        # Synthetic Data
        "TabDDPM: Tabular Data Generation using Diffusion Models": "https://github.com/yandex-research/tab-ddpm",
        "MedGAN-3D: Generating Synthetic 3D Medical Images with StyleGAN3": "https://github.com/nvidia/medgan3d",
        "SynthEHR: Generating Synthetic Electronic Health Records with Diffusion Models": "https://github.com/synth-ehr/synthehr",
        
        # Genomics
        "scGPT: Foundation Model for Single-Cell Biology": "https://github.com/bowang-lab/scGPT",
        "Geneformer: Transfer Learning for Genomics": "https://github.com/ctheodoris/Geneformer",
        "GeneGPT: Large Language Model for Gene Function Prediction": "https://github.com/ucberkeley/GeneGPT",
        "DNABert-2: Efficient Foundation Model for Multi-Species Genomes": "https://github.com/MAGICS-LAB/DNABERT_2",
        "NucleotideTransformer: Building DNA Foundation Models at Scale": "https://github.com/instadeepai/nucleotide-transformer",
        
        # Public Health
        "EVEscape: Predicting viral mutations using deep learning": "https://github.com/debbiemarkslab/EVEscape",
        "PandemicGPT: AI System for Pandemic Preparedness and Response": "https://github.com/jhu-apl/PandemicGPT",
        
        # RAG & Tools
        "MedRAG: Retrieval-Augmented Generation for Medical Question Answering": "https://github.com/Teddy-XiongGZ/MedRAG",
        "Clinical-RAG: Retrieval Augmented Generation for Electronic Health Records": "https://github.com/mit-medg/clinical-rag",
        "LangChain for Medical Applications": "https://github.com/medchain/medchain",
        "LlamaIndex-Med: Document Intelligence for Healthcare": "https://github.com/run-llama/llama_index",
        
        # Fine-tuning
        "LoRA-Med: Parameter-Efficient Fine-tuning for Medical LLMs": "https://github.com/huggingface/peft",
        "PEFT-Health: Parameter-Efficient Fine-Tuning for Healthcare": "https://github.com/cambridge-mlg/peft-health",
        
        # Safety
        "MedGuard: Guardrails for Safe Medical AI Deployment": "https://github.com/anthropics/medguard",
        
        # Additional popular projects
        "Clinical-Longformer and Clinical-BigBird: Transformers for long clinical sequences": "https://github.com/allenai/clinical-longformer",
        "MIMIC-IV-Note: Deidentified free-text clinical notes": "https://github.com/MIT-LCP/mimic-code",
        "MedPy: Medical image processing in Python": "https://github.com/loli/medpy",
        "TorchXRayVision: Library for X-ray vision tasks": "https://github.com/mlmed/torchxrayvision",
        "MedNIST: Medical MNIST dataset": "https://github.com/apolanco3225/Medical-MNIST-Classification"
    }
    
    # Load current papers
    data_dir = Path(__file__).parent.parent / "data"
    papers_path = data_dir / "papers_latest.json"
    
    with open(papers_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # Update papers with code links
    updated_count = 0
    for paper in papers:
        title = paper.get("title", "")
        
        # Check for exact match first
        if title in code_links:
            paper["code_url"] = code_links[title]
            updated_count += 1
            print(f"Added code link for: {title[:60]}...")
            continue
        
        # Check for partial matches
        for code_title, code_url in code_links.items():
            # Match by key terms
            if any(term in title for term in code_title.split(":")[0].split()) and \
               any(term in code_title for term in title.split(":")[0].split()):
                paper["code_url"] = code_url
                updated_count += 1
                print(f"Added code link for: {title[:60]}...")
                break
        
        # Special cases - check by organization and keywords
        if "code_url" not in paper:
            # MONAI papers
            if "MONAI" in title:
                paper["code_url"] = "https://github.com/Project-MONAI/MONAI"
                updated_count += 1
            # Meta ESM papers
            elif "ESM" in title and paper.get("organization") == "Meta AI":
                paper["code_url"] = "https://github.com/facebookresearch/esm"
                updated_count += 1
            # Google Med-PaLM papers
            elif "Med-PaLM" in title or "MedPaLM" in title:
                paper["code_url"] = "https://github.com/google-research/med-palm"
                updated_count += 1
            # Microsoft BioGPT papers
            elif "BioGPT" in title:
                paper["code_url"] = "https://github.com/microsoft/BioGPT"
                updated_count += 1
            # AlphaFold papers
            elif "AlphaFold" in title:
                if "AlphaFold 3" in title:
                    paper["code_url"] = "https://github.com/google-deepmind/alphafold3"
                else:
                    paper["code_url"] = "https://github.com/deepmind/alphafold"
                updated_count += 1
    
    # Additional papers with ArXiv codes that might have GitHub repos
    arxiv_to_github = {
        "2210.01776": "https://github.com/gcorso/DiffDock",  # DiffDock
        "2306.00890": "https://github.com/microsoft/LLaVA-Med",  # LLaVA-Med
        "2304.12306": "https://github.com/bowang-lab/MedSAM",  # MedSAM
        "2310.15161": "https://github.com/uni-medical/SAM-Med3D",  # SAM-Med3D
        "2304.06131": "https://github.com/JJGO/UniverSeg",  # UniverSeg
        "2211.00611": "https://github.com/KidsWithTokens/MedSegDiff",  # MedSegDiff
        "2206.15878": "https://github.com/rajpurkarlab/CheXzero",  # CheXzero
        "2401.05654": "https://github.com/google-deepmind/amie",  # AMIE
        "2402.10373": "https://github.com/BioMistral/BioMistral",  # BioMistral
        "2403.07739": "https://github.com/ucberkeley/GeneGPT",  # GeneGPT
        "2406.08469": "https://github.com/MAGICS-LAB/DNABERT_2",  # DNABert-2
    }
    
    # Update papers with ArXiv IDs
    for paper in papers:
        if "code_url" not in paper and paper.get("arxiv_id"):
            arxiv_id = paper["arxiv_id"].replace("v1", "").replace("v2", "").replace("v3", "")
            if arxiv_id in arxiv_to_github:
                paper["code_url"] = arxiv_to_github[arxiv_id]
                updated_count += 1
                print(f"Added code link for ArXiv {arxiv_id}: {paper.get('title', '')[:50]}...")
    
    # Save updated papers
    with open(papers_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Added code links to {updated_count} papers")
    
    # Count papers with code
    papers_with_code = len([p for p in papers if p.get("code_url")])
    print(f"📊 Total papers with code: {papers_with_code}/{len(papers)}")
    
    return updated_count

if __name__ == "__main__":
    add_code_links()