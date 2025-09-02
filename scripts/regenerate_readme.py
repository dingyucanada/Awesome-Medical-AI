#!/usr/bin/env python3
"""
Complete README regeneration with correct categories
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

def generate_readme():
    """Generate complete README from scratch"""
    data_dir = Path(__file__).parent.parent / "data"
    
    # Load papers
    with open(data_dir / "papers_latest.json", "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    # Load stats
    with open(data_dir / "stats.json", "r", encoding="utf-8") as f:
        stats = json.load(f)
    
    # Define category display names (matching actual data)
    category_names = {
        "foundation_models": "🔬 Foundation Models",
        "clinical_llm": "🏥 Clinical LLMs & Decision Support",
        "medical_imaging": "🩺 Medical Imaging & Vision",
        "patient_interaction": "🤝 Patient Interaction & Engagement",
        "clinical_documentation": "📝 Clinical Documentation & NLP",
        "drug_discovery": "💊 Drug Discovery & Development",
        "ethics_fairness": "⚖️ Ethics, Fairness & Regulation",
        "multimodal": "🎯 Multimodal AI",
        "radiology": "🔍 Radiology & Diagnostics",
        "mental_health": "🧠 Mental Health & Psychiatry",
        "synthetic_data": "📊 Synthetic Data Generation",
        "public_health": "🌍 Public Health & Epidemiology",
        "genomics": "🧬 Genomics & Precision Medicine",
        "data_security_privacy": "🔒 Medical Data Security & Privacy",
        "surgical_robotics": "🤖 Surgical Robotics & IoMT",
        "telemedicine": "📱 Telemedicine & Remote Monitoring",
        "digital_therapeutics": "💚 Digital Therapeutics",
        "wearables": "⌚ Wearable Devices & Health Monitoring"
    }
    
    # Group papers by category
    papers_by_category = {}
    for paper in papers:
        cat = paper.get("category", "unknown")
        if cat not in papers_by_category:
            papers_by_category[cat] = []
        papers_by_category[cat].append(paper)
    
    # Sort papers in each category by year and citations
    for cat in papers_by_category:
        papers_by_category[cat].sort(
            key=lambda x: (
                x.get("year", int(x.get("published", "2023")[:4]) if x.get("published") else 2023),
                x.get("citations", 0)
            ), 
            reverse=True
        )
    
    # Format paper for table
    def format_paper(paper):
        title = paper.get("title", "").replace("|", "-")[:80]
        
        # Create link
        if paper.get("url"):
            title_link = f"[{title}]({paper['url']})"
        elif paper.get("arxiv_id"):
            title_link = f"[{title}](https://arxiv.org/abs/{paper['arxiv_id']})"
        elif paper.get("pmid"):
            title_link = f"[{title}](https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']})"
        else:
            title_link = title
        
        # Date
        if paper.get("published"):
            date = paper.get("published", "")[:10]
        else:
            date = str(paper.get("year", ""))
        
        # Venue/Organization
        venue = paper.get("organization", "")
        if not venue or venue == "Unknown":
            venue = paper.get("journal", "")
            if not venue:
                if "arxiv" in paper.get("source", ""):
                    venue = "arXiv"
                elif "pubmed" in paper.get("source", ""):
                    venue = "PubMed"
                elif paper.get("source") == "curated":
                    venue = "Industry"
                else:
                    venue = "-"
        venue = venue[:25]
        
        # Code
        code = "-"
        if paper.get("code_url"):
            # Shorten GitHub URLs for display
            if "github.com" in paper["code_url"]:
                repo_name = paper["code_url"].split("github.com/")[1].split("/")[1]
                code = f"[{repo_name}]({paper['code_url']})"
            else:
                code = f"[Code]({paper['code_url']})"
        
        # No citations - we don't have real citation data
        
        return f"| {date} | {title_link} | {venue} | {code} |"
    
    # Get recent papers for highlights - always show 5 most recent papers
    # If we have papers from last 30 days, prioritize them
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    recent_in_30_days = sorted(
        [p for p in papers if p.get("published", "")[:10] >= thirty_days_ago],
        key=lambda x: x.get("published", ""),
        reverse=True
    )
    
    # Always get the 5 most recent papers overall
    all_recent = sorted(
        papers,
        key=lambda x: x.get("published", "2020-01-01"),
        reverse=True
    )[:5]
    
    # Combine recent papers from last 30 days with overall recent papers
    # Prioritize papers from last 30 days but ensure we always have 5
    recent_papers = recent_in_30_days[:5]
    if len(recent_papers) < 5:
        # Add more papers from overall recent, avoiding duplicates
        for paper in all_recent:
            if paper not in recent_papers:
                recent_papers.append(paper)
                if len(recent_papers) >= 5:
                    break
    
    highlights = []
    for paper in recent_papers:
        date = paper.get("published", "")[:10]
        # Show more of the title, truncate at word boundary if needed
        full_title = paper.get("title", "")
        if len(full_title) > 120:
            # Truncate at last complete word before 120 chars
            title = full_title[:117] + "..."
        else:
            title = full_title
        
        # Build link - only include if valid
        link = None
        if paper.get("url"):
            link = paper['url']
        elif paper.get("arxiv_id"):
            link = f"https://arxiv.org/abs/{paper['arxiv_id']}"
        elif paper.get("pmid"):
            link = f"https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}"
        
        # Format highlight with or without link
        if link:
            highlights.append(f"- **[{date}]** [{title}]({link})")
        else:
            # Paper without link - show note if available
            note = paper.get("note", "")
            if note:
                highlights.append(f"- **[{date}]** {title} *({note})*")
            else:
                highlights.append(f"- **[{date}]** {title}")
    
    # Generate README content
    readme = f"""# Awesome Medical AI Papers 🏥🤖

![Auto-Update](https://img.shields.io/badge/Auto%20Update-Daily-brightgreen)
![Papers](https://img.shields.io/badge/Papers-{len(papers)}-blue)
![Last Update](https://img.shields.io/badge/Last%20Update-{datetime.now().strftime('%Y--%m--%d')}-orange)

> A comprehensive, auto-updating collection of cutting-edge AI research papers in medicine and healthcare, updated daily via GitHub Actions.

## 🎯 Research Categories

"""
    
    # Add each category section - only show categories with papers
    categories_to_check = ["foundation_models", "clinical_llm", "medical_imaging", "patient_interaction", 
                   "clinical_documentation", "drug_discovery", "ethics_fairness", "multimodal",
                   "radiology", "mental_health", "synthetic_data", "public_health", "genomics",
                   "data_security_privacy", "surgical_robotics", "telemedicine", "digital_therapeutics", "wearables"]
    
    for cat_key in categories_to_check:
        cat_papers = papers_by_category.get(cat_key, [])[:15]  # Top 15 per category
        
        # Only include categories that have papers
        if cat_papers:
            cat_name = category_names.get(cat_key, cat_key)
            readme += f"### {cat_name}\n\n"
            readme += "| Date | Title | Venue/Org | Code |\n"
            readme += "|------|-------|-----------|------|\n"
            
            for paper in cat_papers:
                readme += format_paper(paper) + "\n"
            
            readme += "\n"
    
    # Add statistics section
    papers_with_code = len([p for p in papers if p.get("code_url")])
    
    readme += f"""## 📈 Statistics & Trends

### Collection Overview
- **Total Papers**: {stats['total_papers']}
- **Papers with Code**: {papers_with_code}
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d')}

### Papers by Year
"""
    
    for year in sorted(stats['by_year'].keys(), reverse=True):
        readme += f"- **{year}**: {stats['by_year'][year]} papers\n"
    
    readme += "\n### Top Organizations\n"
    top_orgs = sorted(stats['by_organization'].items(), key=lambda x: x[1], reverse=True)
    for org, count in top_orgs[:10]:
        if count > 1 and org != "Unknown":
            readme += f"- **{org}**: {count} papers\n"
    
    readme += """
### Most Active Categories
"""
    for cat, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)[:5]:
        cat_display = category_names.get(cat, cat)
        readme += f"- {cat_display}: {count} papers\n"
    
    readme += """
## 🔔 Subscribe to Updates

Watch this repository to get notified of new papers!

## 📚 Resources

- [Survey Paper](SURVEY.md) - Auto-generated comprehensive survey
- [API Documentation](docs/API.md) - Access our data programmatically  
- [Contributing Guidelines](CONTRIBUTING.md) - Help improve this collection

## 🤖 Automation Details & AI Technology Stack

This repository updates automatically every day at 00:00 UTC through GitHub Actions:

### Data Sources
- **APIs**: ArXiv, PubMed, MedRxiv, BioRxiv, Semantic Scholar
- **Institutional**: Google Scholar, Microsoft Academic, Clinical Trials
- **Industry**: Company research blogs, GitHub releases

### AI Tools & Frameworks Covered
- **RAG Systems**: LangChain, LlamaIndex, Haystack, vector databases (Pinecone, Weaviate, Chroma)
- **AI Agents**: AutoGPT, BabyAGI, SuperAGI, CrewAI, Microsoft AutoGen
- **Model Frameworks**: Hugging Face, OpenAI API, Anthropic Claude, Google Vertex AI
- **Fine-tuning**: LoRA, QLoRA, PEFT, Adapters, Prefix Tuning
- **Deployment**: TorchServe, Triton, BentoML, Ray Serve, vLLM
- **Orchestration**: Apache Airflow, Prefect, Dagster, Kubeflow
- **MLOps**: MLflow, Weights & Biases, Neptune, ClearML
- **Safety**: Guardrails AI, NeMo Guardrails, Constitutional AI
- **Embeddings**: Sentence Transformers, OpenAI Embeddings, Cohere Embed
- **Prompt Engineering**: DSPy, Guidance, Promptify, LangChain Templates
- **Knowledge Graphs**: Neo4j, Amazon Neptune, GraphRAG
- **Model Compression**: Quantization, Distillation, Pruning, ONNX

### Search Keywords (100+ terms)
- **Foundation Models**: GPT-4, Claude, Gemini, Llama, Mistral, Falcon, Mixtral
- **Medical LLMs**: Med-PaLM, BioGPT, ClinicalBERT, BioBERT, PubMedBERT
- **AI Techniques**: RAG, Fine-tuning, Few-shot, Zero-shot, Chain-of-Thought, RLHF
- **Machine Learning**: Deep learning, Computer vision, NLP, Federated learning
- **Clinical Applications**: Decision support, Diagnosis, Treatment planning, Risk prediction
- **Medical Imaging**: Radiology AI, Pathology AI, Medical computer vision
- **Healthcare Data**: EHR analysis, Wearable devices, Genomics, Proteomics

## 📊 Key Research Areas

- **Foundation Models**: Large language models for medicine (Med-PaLM, BioGPT, clinical LLMs)
- **Medical Imaging & Vision**: AI for radiology, pathology, medical image analysis
- **Clinical Decision Support**: Diagnosis assistance, treatment recommendation, risk assessment
- **Drug Discovery & Development**: Molecular modeling, virtual screening, drug design
- **Healthcare Data Analytics**: EHR analysis, population health, predictive modeling
- **Wearable & Remote Monitoring**: IoT sensors, continuous monitoring, digital biomarkers
- **Medical Data Security**: Federated learning, differential privacy, secure computation
- **Ethics & Regulation**: AI safety, bias mitigation, FDA compliance, fairness

---
*Maintained with ❤️ by the research community | Powered by GitHub Actions*
"""
    
    # Save README
    readme_path = Path(__file__).parent.parent / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme)
    
    print(f"README regenerated successfully!")
    print(f"- Total papers: {len(papers)}")
    print(f"- Categories with papers: {len([c for c in papers_by_category if papers_by_category[c]])}")
    
    # Show category distribution
    print("\nCategory distribution:")
    for cat_key, cat_name in category_names.items():
        count = len(papers_by_category.get(cat_key, []))
        if count > 0:
            print(f"  {cat_name}: {count} papers")

if __name__ == "__main__":
    generate_readme()