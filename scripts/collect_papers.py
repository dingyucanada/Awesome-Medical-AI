#!/usr/bin/env python3
"""
Automated paper collection for Generative AI in Healthcare
Collects from: ArXiv, PubMed, BioRxiv, MedRxiv
"""

import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
import time
from pathlib import Path
import hashlib

class HealthcareAIPaperCollector:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Healthcare-specific keywords
        self.keywords = [
            "generative AI healthcare",
            "LLM medical", "LLM clinical",
            "GPT healthcare", "GPT medical",
            "diffusion model medical imaging",
            "generative model drug discovery",
            "clinical NLP", "medical text generation",
            "AI diagnosis", "AI treatment planning",
            "medical chatbot", "healthcare assistant",
            "synthetic medical data",
            "federated learning healthcare"
        ]
        
        self.categories = {
            "clinical_apps": ["diagnosis", "treatment", "prognosis", "clinical decision", "EHR"],
            "drug_discovery": ["drug", "molecule", "compound", "pharmaceutical", "discovery"],
            "medical_imaging": ["imaging", "radiology", "CT", "MRI", "X-ray", "ultrasound", "pathology"],
            "documentation": ["clinical notes", "medical report", "documentation", "summarization"],
            "genomics": ["genomic", "genetic", "precision medicine", "personalized", "biomarker"],
            "patient_care": ["patient", "chatbot", "communication", "education", "engagement"],
            "ethics": ["ethics", "bias", "privacy", "fairness", "regulation", "safety"],
            "foundation": ["foundation model", "base model", "pretrain", "architecture"]
        }
        
    def collect_arxiv_papers(self, max_results: int = 100) -> List[Dict]:
        """Collect papers from ArXiv"""
        papers = []
        base_url = "http://export.arxiv.org/api/query"
        
        # Healthcare-specific ArXiv categories
        categories = ["cs.AI", "cs.LG", "cs.CL", "q-bio", "stat.ML"]
        
        for keyword in self.keywords[:5]:  # Limit queries to avoid rate limiting
            query = f"all:{keyword}"
            params = {
                "search_query": query,
                "start": 0,
                "max_results": min(max_results // len(self.keywords), 20),
                "sortBy": "submittedDate",
                "sortOrder": "descending"
            }
            
            try:
                response = requests.get(base_url, params=params, timeout=30)
                if response.status_code == 200:
                    papers.extend(self._parse_arxiv_response(response.text))
                time.sleep(3)  # Rate limiting
            except Exception as e:
                print(f"Error fetching ArXiv papers: {e}")
                
        return papers
    
    def _parse_arxiv_response(self, xml_content: str) -> List[Dict]:
        """Parse ArXiv API response"""
        papers = []
        
        # Simple XML parsing (in production, use proper XML parser)
        entries = xml_content.split("<entry>")[1:]
        
        for entry in entries:
            try:
                paper = {
                    "source": "arxiv",
                    "title": self._extract_xml_field(entry, "title"),
                    "abstract": self._extract_xml_field(entry, "summary"),
                    "authors": self._extract_authors(entry),
                    "published": self._extract_xml_field(entry, "published")[:10],
                    "updated": self._extract_xml_field(entry, "updated")[:10],
                    "arxiv_id": self._extract_arxiv_id(entry),
                    "pdf_url": self._extract_pdf_url(entry),
                    "categories": self._extract_categories(entry),
                    "paper_id": None,
                    "citations": 0,  # ArXiv doesn't provide citations directly
                    "journal": "arXiv"  # Set journal for consistency
                }
                
                # Generate unique ID
                paper["paper_id"] = hashlib.md5(
                    f"{paper['title']}_{paper['published']}".encode()
                ).hexdigest()[:12]
                
                # Auto-categorize
                paper["category"] = self._categorize_paper(paper)
                
                papers.append(paper)
            except Exception as e:
                print(f"Error parsing entry: {e}")
                continue
                
        return papers
    
    def _extract_xml_field(self, content: str, field: str) -> str:
        """Extract field from XML content"""
        pattern = f"<{field}>(.*?)</{field}>"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip().replace("\n", " ")
        return ""
    
    def _extract_authors(self, content: str) -> List[str]:
        """Extract authors from XML"""
        authors = []
        author_matches = re.findall(r"<name>(.*?)</name>", content)
        return author_matches
    
    def _extract_arxiv_id(self, content: str) -> str:
        """Extract ArXiv ID"""
        match = re.search(r"<id>.*?([0-9]+\.[0-9]+v?[0-9]*)</id>", content)
        return match.group(1) if match else ""
    
    def _extract_pdf_url(self, content: str) -> str:
        """Extract PDF URL"""
        arxiv_id = self._extract_arxiv_id(content)
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf" if arxiv_id else ""
    
    def _extract_categories(self, content: str) -> List[str]:
        """Extract paper categories"""
        matches = re.findall(r'<category.*?term="([^"]+)"', content)
        return matches
    
    def _categorize_paper(self, paper: Dict) -> str:
        """Categorize paper based on content"""
        text = (paper["title"] + " " + paper["abstract"]).lower()
        
        scores = {}
        for category, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[category] = score
        
        if scores:
            return max(scores, key=scores.get)
        return "foundation"  # Default category
    
    def collect_pubmed_papers(self, max_results: int = 50) -> List[Dict]:
        """Collect papers from PubMed (simplified version)"""
        papers = []
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        
        # PubMed search for generative AI in healthcare
        search_terms = [
            "generative artificial intelligence",
            "large language model clinical",
            "GPT healthcare",
            "diffusion model medical",
            "synthetic medical data"
        ]
        
        for term in search_terms[:3]:  # Limit to avoid rate limiting
            try:
                # Search for IDs
                search_url = f"{base_url}/esearch.fcgi"
                search_params = {
                    "db": "pubmed",
                    "term": term,
                    "retmax": max_results // len(search_terms),
                    "retmode": "json",
                    "sort": "pub_date"
                }
                
                response = requests.get(search_url, params=search_params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    id_list = data.get("esearchresult", {}).get("idlist", [])
                    
                    if id_list:
                        # Fetch details
                        fetch_url = f"{base_url}/efetch.fcgi"
                        fetch_params = {
                            "db": "pubmed",
                            "id": ",".join(id_list[:10]),  # Limit to 10 papers per query
                            "retmode": "xml"
                        }
                        
                        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
                        if fetch_response.status_code == 200:
                            papers.extend(self._parse_pubmed_response(fetch_response.text))
                    
                time.sleep(1)  # Rate limiting for NCBI
                
            except Exception as e:
                print(f"Error fetching PubMed papers: {e}")
                
        return papers
    
    def _parse_pubmed_response(self, xml_content: str) -> List[Dict]:
        """Parse PubMed XML response (simplified)"""
        papers = []
        
        articles = xml_content.split("<PubmedArticle>")[1:]
        
        for article in articles[:10]:  # Process up to 10 articles
            try:
                pmid = self._extract_xml_field(article, "PMID")
                paper = {
                    "source": "pubmed",
                    "title": self._extract_xml_field(article, "ArticleTitle"),
                    "abstract": self._extract_xml_field(article, "AbstractText"),
                    "published": self._extract_pubmed_date(article),
                    "journal": self._extract_xml_field(article, "Title"),
                    "pmid": pmid,
                    "pdf_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
                    "paper_id": None,
                    "citations": 0  # PubMed doesn't provide citation count in basic API
                }
                
                # Generate unique ID
                paper["paper_id"] = hashlib.md5(
                    f"{paper['title']}_{paper['published']}".encode()
                ).hexdigest()[:12]
                
                # Auto-categorize
                paper["category"] = self._categorize_paper(paper)
                
                if paper["title"]:  # Only add if title exists
                    papers.append(paper)
                    
            except Exception as e:
                print(f"Error parsing PubMed article: {e}")
                
        return papers
    
    def _extract_pubmed_date(self, content: str) -> str:
        """Extract publication date from PubMed article"""
        year = self._extract_xml_field(content, "Year") or "2025"
        month = self._extract_xml_field(content, "Month") or "01"
        day = self._extract_xml_field(content, "Day") or "01"
        
        # Convert month name to number if necessary
        months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", 
                 "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                 "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        month = months.get(month, month)
        
        try:
            return f"{year}-{month:0>2}-{day:0>2}"
        except:
            return "2025-01-01"
    
    def remove_duplicates(self, papers: List[Dict]) -> List[Dict]:
        """Remove duplicate papers based on title similarity"""
        seen_ids = set()
        unique_papers = []
        
        for paper in papers:
            if paper["paper_id"] not in seen_ids:
                seen_ids.add(paper["paper_id"])
                unique_papers.append(paper)
                
        return unique_papers
    
    def save_papers(self, papers: List[Dict]) -> None:
        """Save papers to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save with timestamp
        filepath = self.data_dir / f"papers_{timestamp}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        # Also save as latest
        latest_filepath = self.data_dir / "papers_latest.json"
        with open(latest_filepath, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(papers)} papers to {filepath}")
    
    def load_existing_papers(self) -> List[Dict]:
        """Load existing papers from latest file"""
        latest_filepath = self.data_dir / "papers_latest.json"
        if latest_filepath.exists():
            with open(latest_filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def merge_papers(self, new_papers: List[Dict], existing_papers: List[Dict]) -> List[Dict]:
        """Merge new papers with existing ones"""
        all_papers = existing_papers + new_papers
        return self.remove_duplicates(all_papers)
    
    def run(self):
        """Main collection process"""
        print("Starting Healthcare AI paper collection...")
        
        # Load existing papers
        existing_papers = self.load_existing_papers()
        print(f"Loaded {len(existing_papers)} existing papers")
        
        # Collect new papers
        print("Collecting from ArXiv...")
        arxiv_papers = self.collect_arxiv_papers()
        print(f"Found {len(arxiv_papers)} ArXiv papers")
        
        print("Collecting from PubMed...")
        pubmed_papers = self.collect_pubmed_papers()
        print(f"Found {len(pubmed_papers)} PubMed papers")
        
        # Merge all papers
        all_new_papers = arxiv_papers + pubmed_papers
        all_papers = self.merge_papers(all_new_papers, existing_papers)
        
        # Sort by date (newest first)
        all_papers.sort(key=lambda x: x.get("published", ""), reverse=True)
        
        # Save papers
        self.save_papers(all_papers)
        
        # Generate statistics
        stats = {
            "total_papers": len(all_papers),
            "new_papers": len(all_new_papers),
            "by_source": {},
            "by_category": {},
            "last_updated": datetime.now().isoformat()
        }
        
        for paper in all_papers:
            source = paper.get("source", "unknown")
            category = paper.get("category", "uncategorized")
            stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        
        # Save statistics
        stats_filepath = self.data_dir / "stats.json"
        with open(stats_filepath, "w") as f:
            json.dump(stats, f, indent=2)
        
        print(f"\nCollection complete!")
        print(f"Total papers: {stats['total_papers']}")
        print(f"New papers: {stats['new_papers']}")
        print(f"By source: {stats['by_source']}")
        print(f"By category: {stats['by_category']}")

if __name__ == "__main__":
    collector = HealthcareAIPaperCollector()
    collector.run()