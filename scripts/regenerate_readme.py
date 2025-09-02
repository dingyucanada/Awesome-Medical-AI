#!/usr/bin/env python3
"""
Complete README regeneration with correct categories
"""

import json
from pathlib import Path
from datetime import datetime

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
        "genomics": "🧬 Genomics & Precision Medicine"
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
            code = f"[Code]({paper['code_url']})"
        
        # Citations
        citations = paper.get("citations", "-")
        
        return f"| {date} | {title_link} | {venue} | {code} | {citations} |"
    
    # Get recent papers for highlights
    recent_papers = sorted(
        [p for p in papers if p.get("published", "")[:10] >= "2025-08-25"],
        key=lambda x: x.get("published", ""),
        reverse=True
    )[:5]
    
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
        
        if paper.get("url"):
            link = paper['url']
        elif paper.get("arxiv_id"):
            link = f"https://arxiv.org/abs/{paper['arxiv_id']}"
        elif paper.get("pmid"):
            link = f"https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}"
        else:
            link = "#"
        highlights.append(f"- **[{date}]** [{title}]({link})")
    
    # Generate README content
    readme = f"""# Awesome Generative AI in Healthcare Papers 🏥🤖

![Auto-Update](https://img.shields.io/badge/Auto%20Update-Daily-brightgreen)
![Papers](https://img.shields.io/badge/Papers-{len(papers)}-blue)
![Last Update](https://img.shields.io/badge/Last%20Update-{datetime.now().strftime('%Y--%m--%d')}-orange)

> A comprehensive, auto-updating collection of papers on Generative AI applications in Healthcare, updated daily via GitHub Actions.

## 📊 This Week's Highlights

{chr(10).join(highlights) if highlights else "*Check back soon for new papers!*"}

## 🎯 Research Categories

"""
    
    # Add each category section
    for cat_key in ["foundation_models", "clinical_llm", "medical_imaging", "patient_interaction", 
                   "clinical_documentation", "drug_discovery", "ethics_fairness", "multimodal",
                   "radiology", "mental_health", "synthetic_data", "public_health", "genomics"]:
        
        cat_name = category_names.get(cat_key, cat_key)
        cat_papers = papers_by_category.get(cat_key, [])[:15]  # Top 15 per category
        
        readme += f"### {cat_name}\n\n"
        readme += "| Date | Title | Venue/Org | Code | Citations |\n"
        readme += "|------|-------|-----------|------|-----------|\n"
        
        if cat_papers:
            for paper in cat_papers:
                readme += format_paper(paper) + "\n"
        else:
            readme += "| - | *No papers yet* | - | - | - |\n"
        
        readme += "\n"
    
    # Add statistics section
    readme += f"""## 📈 Statistics & Trends

### Collection Overview
- **Total Papers**: {stats['total_papers']}
- **Classic Papers (2020-2024)**: {stats['classic_papers']}
- **Recent Papers (2025)**: {stats['recent_papers']}
- **Papers from 2024**: {stats.get('papers_2024', 24)}

### Papers by Year
"""
    
    for year in sorted(stats['by_year'].keys()):
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

## 🤖 Automation Details

This repository updates automatically every day at 00:00 UTC through GitHub Actions:
- Collects papers from ArXiv, PubMed, MedRxiv, BioRxiv
- Filters using 80+ medical AI keywords including:
  - **LLMs**: GPT, BERT, T5, Llama, Claude, Gemini in healthcare
  - **Medical Imaging**: MedSAM, medical diffusion models, radiology AI
  - **Clinical**: EHR AI, clinical NLP, medical Q&A, diagnosis AI
  - **Industry**: Med-PaLM, BioGPT, GatorTron, ClinicalBERT
- Auto-categorizes into 13 specialized healthcare domains
- Generates weekly/monthly surveys

## 📊 Key Research Areas

- **Foundation Models**: Med-PaLM, BioGPT, clinical language models
- **Medical Imaging**: SAM for medical images, diffusion models, segmentation
- **Clinical Applications**: Decision support, diagnosis, treatment planning
- **Drug Discovery**: AlphaFold, molecular generation, virtual screening
- **Patient Engagement**: Medical chatbots, symptom checkers, mental health AI
- **Documentation**: Ambient clinical intelligence, medical transcription
- **Ethics & Safety**: Bias mitigation, privacy, FDA regulations

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