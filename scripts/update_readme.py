#!/usr/bin/env python3
"""
Update README.md with collected papers
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import re

class ReadmeUpdater:
    def __init__(self):
        self.project_dir = Path(__file__).parent.parent
        self.data_dir = self.project_dir / "data"
        self.readme_path = self.project_dir / "README.md"
        
        self.category_mapping = {
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
        
    def load_papers(self) -> List[Dict]:
        """Load papers from latest JSON file"""
        latest_filepath = self.data_dir / "papers_latest.json"
        if latest_filepath.exists():
            with open(latest_filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def load_stats(self) -> Dict:
        """Load statistics"""
        stats_filepath = self.data_dir / "stats.json"
        if stats_filepath.exists():
            with open(stats_filepath, "r") as f:
                return json.load(f)
        return {}
    
    def format_paper_row(self, paper: Dict) -> str:
        """Format a paper as a markdown table row"""
        title = paper.get("title", "").replace("|", "-")[:100]
        
        # Create links - handle missing links properly
        if paper.get("url"):
            title_link = f"[{title}]({paper['url']})"
        elif paper.get("arxiv_id"):
            title_link = f"[{title}](https://arxiv.org/abs/{paper['arxiv_id']})"
        elif paper.get("pmid"):
            title_link = f"[{title}](https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']})"
        elif paper.get("pdf_url"):
            title_link = f"[{title}]({paper['pdf_url']})"
        else:
            # For papers without links, just show title
            title_link = title
        
        # Format date
        date = paper.get("published", "")[:10] if paper.get("published") else str(paper.get("year", ""))
        
        # Venue (enhanced detection)
        venue = paper.get("journal", "")
        if not venue:
            if paper.get("organization") and paper.get("organization") != "Unknown":
                venue = paper.get("organization", "")[:25]
            elif "arxiv" in paper.get("source", ""):
                venue = "arXiv"
            elif "pubmed" in paper.get("source", ""):
                venue = "PubMed"
            elif paper.get("source") == "curated":
                venue = "Industry/Lab"
            else:
                venue = paper.get("source", "").title()
        venue = venue[:30] if venue else "-"
        
        # Code detection (check for common code indicators)
        code = "-"
        abstract = paper.get("abstract", "").lower()
        if any(term in abstract for term in ["github.com", "code available", "implementation"]):
            code = "[Code*]"  # Asterisk indicates potential code availability
        
        # Citations (show if available, otherwise dash)
        citations = paper.get("citations", "-")
        if citations == 0:
            citations = "0"
        elif citations == "-" or not citations:
            citations = "-"
        
        return f"| {date} | {title_link} | {venue} | {code} | {citations} |"
    
    def get_recent_papers(self, papers: List[Dict], days: int = 7) -> List[Dict]:
        """Get papers from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent = []
        
        for paper in papers:
            try:
                pub_date = datetime.strptime(paper.get("published", "")[:10], "%Y-%m-%d")
                if pub_date >= cutoff_date:
                    recent.append(paper)
            except:
                continue
                
        return recent
    
    def update_readme(self):
        """Update README.md with latest papers"""
        print("Updating README.md...")
        
        # Load data
        papers = self.load_papers()
        stats = self.load_stats()
        
        if not papers:
            print("No papers found. Run collect_papers.py first.")
            return
        
        # Read current README
        with open(self.readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        
        # Update badges
        readme_content = re.sub(
            r"!\[Papers\]\(.*?\)",
            f"![Papers](https://img.shields.io/badge/Papers-{len(papers)}-blue)",
            readme_content
        )
        
        readme_content = re.sub(
            r"!\[Last Update\]\(.*?\)",
            f"![Last Update](https://img.shields.io/badge/Last%20Update-{datetime.now().strftime('%Y--%m--%d')}-orange)",
            readme_content
        )
        
        # Update This Week's Highlights
        recent_papers = self.get_recent_papers(papers, days=7)
        highlights = []
        for paper in recent_papers[:5]:  # Top 5 recent papers
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
        
        if highlights:
            highlights_text = "\n".join(highlights)
        else:
            highlights_text = "*No new papers this week. Check back soon!*"
        
        # Update highlights section
        readme_content = re.sub(
            r"## 📊 This Week's Highlights\n\n.*?(?=\n##)",
            f"## 📊 This Week's Highlights\n\n{highlights_text}\n",
            readme_content,
            flags=re.DOTALL
        )
        
        # Group papers by category
        papers_by_category = {}
        for paper in papers:
            category = paper.get("category", "foundation")
            if category not in papers_by_category:
                papers_by_category[category] = []
            papers_by_category[category].append(paper)
        
        # Update each category section
        for category_key, category_title in self.category_mapping.items():
            category_papers = papers_by_category.get(category_key, [])
            
            # Sort by date (newest first) and take top 20
            category_papers.sort(key=lambda x: x.get("published", ""), reverse=True)
            category_papers = category_papers[:20]
            
            # Create table rows
            if category_papers:
                rows = [self.format_paper_row(p) for p in category_papers]
                table_content = "\n".join(rows)
            else:
                table_content = "| | *No papers yet* | | | |"
            
            # Update section in README
            pattern = f"### {re.escape(category_title)}.*?\n\| Date \| Title \| Venue \| Code \| Citations \|\n\|.*?\|\n(.*?)(?=\n###|\n##|\Z)"
            replacement = f"### {category_title}\nPapers focusing on {category_title.split(' ', 1)[1].lower()}.\n\n| Date | Title | Venue | Code | Citations |\n|------|-------|-------|------|-----------|\n{table_content}"
            
            readme_content = re.sub(
                pattern,
                replacement,
                readme_content,
                flags=re.DOTALL
            )
        
        # Update statistics
        total_papers = stats.get("total_papers", 0)
        by_source = stats.get("by_source", {})
        by_category = stats.get("by_category", {})
        
        # Find top venues (simplified - in production, extract actual venues)
        top_venues = []
        if "arxiv" in by_source:
            top_venues.append(f"arXiv ({by_source['arxiv']})")
        if "pubmed" in by_source:
            top_venues.append(f"PubMed ({by_source['pubmed']})")
        
        # Find trending keywords (simplified)
        trending = ["LLM", "GPT-4", "Clinical AI", "Medical Imaging", "Drug Discovery"]
        
        stats_text = f"""### Monthly Statistics
- Total Papers: {total_papers}
- Top Venues: {', '.join(top_venues) if top_venues else '*TBD*'}
- Most Active Categories: {', '.join([k for k, v in sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:3]])}
- Trending Keywords: {', '.join(trending)}"""
        
        readme_content = re.sub(
            r"### Monthly Statistics.*?(?=\n###|\n##|\Z)",
            stats_text + "\n",
            readme_content,
            flags=re.DOTALL
        )
        
        # Save updated README
        with open(self.readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print(f"README.md updated successfully!")
        print(f"- Total papers: {total_papers}")
        print(f"- Recent papers (7 days): {len(recent_papers)}")
        print(f"- Categories updated: {len(papers_by_category)}")

if __name__ == "__main__":
    updater = ReadmeUpdater()
    updater.update_readme()