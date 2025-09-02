#!/usr/bin/env python3
"""
Fix missing PMIDs and fetch citation counts for papers
"""

import json
import requests
import time
from pathlib import Path
from typing import Dict, List
import re
import hashlib

class PaperFixer:
    def __init__(self):
        self.project_dir = Path(__file__).parent.parent
        self.data_dir = self.project_dir / "data"
        
    def load_papers(self) -> List[Dict]:
        """Load papers from latest JSON file"""
        latest_filepath = self.data_dir / "papers_latest.json"
        if latest_filepath.exists():
            with open(latest_filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def fetch_pmid_from_title(self, title: str) -> str:
        """Fetch PMID using title search"""
        try:
            # Clean title for search
            clean_title = re.sub(r'[^\w\s]', ' ', title)
            clean_title = ' '.join(clean_title.split()[:10])  # Use first 10 words
            
            # Search PubMed for the paper
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": clean_title,
                "retmax": 1,
                "retmode": "json"
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                id_list = data.get("esearchresult", {}).get("idlist", [])
                if id_list:
                    return id_list[0]
            
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"Error fetching PMID for '{title[:50]}...': {e}")
        
        return ""
    
    def fetch_citations_from_semantic_scholar(self, title: str, arxiv_id: str = None) -> int:
        """Fetch citation count from Semantic Scholar API"""
        try:
            # Try ArXiv ID first if available
            if arxiv_id:
                url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}"
                params = {"fields": "citationCount"}
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("citationCount", 0)
            
            # Fallback to title search
            search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": title[:100],  # Limit title length
                "fields": "citationCount",
                "limit": 1
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                papers = data.get("data", [])
                if papers:
                    return papers[0].get("citationCount", 0)
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error fetching citations for '{title[:50]}...': {e}")
        
        return 0
    
    def fetch_arxiv_citations(self, arxiv_id: str) -> int:
        """Fetch citations for ArXiv paper"""
        try:
            # Use Semantic Scholar API for ArXiv papers
            url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}"
            params = {"fields": "citationCount,title"}
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("citationCount", 0)
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error fetching ArXiv citations for {arxiv_id}: {e}")
        
        return 0
    
    def fix_papers(self):
        """Fix missing PMIDs and add citation counts"""
        papers = self.load_papers()
        
        if not papers:
            print("No papers found")
            return
        
        print(f"Fixing {len(papers)} papers...")
        
        fixed_count = 0
        citation_count = 0
        
        for i, paper in enumerate(papers):
            print(f"Processing {i+1}/{len(papers)}: {paper.get('title', '')[:50]}...")
            
            # Fix missing PMIDs for PubMed papers
            if paper.get("source") == "pubmed" and not paper.get("pmid"):
                pmid = self.fetch_pmid_from_title(paper.get("title", ""))
                if pmid:
                    paper["pmid"] = pmid
                    paper["pdf_url"] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    fixed_count += 1
                    print(f"  ✓ Found PMID: {pmid}")
            
            # Fetch citation counts
            if paper.get("source") == "arxiv" and paper.get("arxiv_id"):
                citations = self.fetch_arxiv_citations(paper.get("arxiv_id"))
                if citations > 0:
                    paper["citations"] = citations
                    citation_count += 1
                    print(f"  ✓ Citations: {citations}")
            elif paper.get("title"):
                citations = self.fetch_citations_from_semantic_scholar(
                    paper.get("title", ""),
                    paper.get("arxiv_id")
                )
                if citations > 0:
                    paper["citations"] = citations
                    citation_count += 1
                    print(f"  ✓ Citations: {citations}")
            
            # Add a small delay to avoid rate limiting
            if i % 10 == 0 and i > 0:
                print("  Pausing to avoid rate limits...")
                time.sleep(2)
        
        # Save updated papers
        output_path = self.data_dir / "papers_latest.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Fixed {fixed_count} PMIDs")
        print(f"✅ Added {citation_count} citation counts")
        print(f"✅ Saved to {output_path}")
        
        return papers

if __name__ == "__main__":
    fixer = PaperFixer()
    fixer.fix_papers()