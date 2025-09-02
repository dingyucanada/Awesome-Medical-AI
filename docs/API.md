# 🔌 API Documentation

Access the Healthcare AI papers collection programmatically through our JSON data endpoints.

## Quick Start

### Get All Papers
```bash
curl https://raw.githubusercontent.com/dingyucanada/Awesome-GenAI-Healthcare/main/data/papers_latest.json
```

### Get Statistics
```bash
curl https://raw.githubusercontent.com/dingyucanada/Awesome-GenAI-Healthcare/main/data/stats.json
```

## Data Structure

### Paper Object

Each paper in the collection contains the following fields:

```json
{
  "paper_id": "unique_identifier",
  "title": "Paper title",
  "abstract": "Paper abstract text",
  "authors": ["Author 1", "Author 2"],
  "published": "2025-08-29",
  "source": "arxiv|pubmed",
  "category": "medical_imaging|clinical_apps|...",
  "citations": 10,
  
  // Source-specific fields
  "arxiv_id": "2508.21824v1",        // For ArXiv papers
  "pdf_url": "https://...",          // Direct PDF link
  "pmid": "39218386",                // For PubMed papers
  "journal": "Journal name"          // Journal/venue name
}
```

### Categories

Papers are classified into 8 categories:

- `clinical_apps` - Clinical Applications
- `drug_discovery` - Drug Discovery & Development  
- `medical_imaging` - Medical Imaging
- `documentation` - Clinical Documentation
- `genomics` - Genomics & Precision Medicine
- `patient_care` - Patient Care & Engagement
- `ethics` - Ethics, Safety & Regulation
- `foundation` - Foundational Models

## Python Examples

### Load and Filter Papers

```python
import requests
import json

# Fetch all papers
response = requests.get(
    "https://raw.githubusercontent.com/dingyucanada/Awesome-GenAI-Healthcare/main/data/papers_latest.json"
)
papers = response.json()

# Filter by category
imaging_papers = [p for p in papers if p["category"] == "medical_imaging"]

# Filter by date (last 30 days)
from datetime import datetime, timedelta
cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
recent = [p for p in papers if p["published"] >= cutoff]

# Sort by citations
top_cited = sorted(papers, key=lambda x: x.get("citations", 0), reverse=True)[:10]
```

### Search Papers

```python
def search_papers(papers, query):
    """Search papers by title or abstract"""
    query = query.lower()
    results = []
    
    for paper in papers:
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower()
        
        if query in title or query in abstract:
            results.append(paper)
    
    return results

# Example: Find papers about LLMs
llm_papers = search_papers(papers, "large language model")
```

### Get Papers by Source

```python
# Get ArXiv papers only
arxiv_papers = [p for p in papers if p["source"] == "arxiv"]

# Get PubMed papers only  
pubmed_papers = [p for p in papers if p["source"] == "pubmed"]
```

## JavaScript Examples

### Fetch and Display Papers

```javascript
// Fetch papers
fetch('https://raw.githubusercontent.com/dingyucanada/Awesome-GenAI-Healthcare/main/data/papers_latest.json')
  .then(response => response.json())
  .then(papers => {
    // Filter recent papers
    const today = new Date();
    const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
    
    const recentPapers = papers.filter(p => {
      return new Date(p.published) >= weekAgo;
    });
    
    console.log(`Found ${recentPapers.length} papers from last week`);
  });
```

### Create Custom Dashboard

```javascript
async function createDashboard() {
  const response = await fetch(
    'https://raw.githubusercontent.com/dingyucanada/Awesome-GenAI-Healthcare/main/data/papers_latest.json'
  );
  const papers = await response.json();
  
  // Group by category
  const byCategory = {};
  papers.forEach(paper => {
    const cat = paper.category;
    if (!byCategory[cat]) byCategory[cat] = [];
    byCategory[cat].push(paper);
  });
  
  // Display statistics
  Object.entries(byCategory).forEach(([category, papers]) => {
    console.log(`${category}: ${papers.length} papers`);
  });
}
```

## R Examples

```r
library(jsonlite)
library(dplyr)

# Load papers
papers_url <- "https://raw.githubusercontent.com/dingyucanada/Awesome-GenAI-Healthcare/main/data/papers_latest.json"
papers <- fromJSON(papers_url)

# Convert to dataframe
papers_df <- as.data.frame(papers)

# Analyze by category
category_summary <- papers_df %>%
  group_by(category) %>%
  summarise(
    count = n(),
    avg_citations = mean(citations, na.rm = TRUE)
  )

# Top cited papers
top_papers <- papers_df %>%
  arrange(desc(citations)) %>%
  head(10) %>%
  select(title, citations, published)
```

## Rate Limits

The data is hosted on GitHub's raw content service:
- No authentication required
- Standard GitHub rate limits apply
- Consider caching responses locally
- Update frequency: Daily at 00:00 UTC

## Data Updates

- **Frequency**: Daily automatic updates
- **New papers**: Added from ArXiv and PubMed
- **Citations**: Updated periodically
- **Categories**: Automatically assigned using ML

## Building Your Own Tools

### Example: Email Notification Service

```python
import requests
import json
from datetime import datetime, timedelta

def get_new_papers(days=1):
    """Get papers from the last N days"""
    response = requests.get(
        "https://raw.githubusercontent.com/dingyucanada/Awesome-GenAI-Healthcare/main/data/papers_latest.json"
    )
    papers = response.json()
    
    cutoff = datetime.now() - timedelta(days=days)
    new_papers = []
    
    for paper in papers:
        pub_date = datetime.strptime(paper["published"], "%Y-%m-%d")
        if pub_date >= cutoff:
            new_papers.append(paper)
    
    return new_papers

# Get today's papers
today_papers = get_new_papers(1)
if today_papers:
    print(f"Found {len(today_papers)} new papers!")
    # Send email notification...
```

### Example: Citation Tracker

```python
def track_citations(paper_id):
    """Track citation changes for a specific paper"""
    response = requests.get(
        "https://raw.githubusercontent.com/dingyucanada/Awesome-GenAI-Healthcare/main/data/papers_latest.json"
    )
    papers = response.json()
    
    for paper in papers:
        if paper["paper_id"] == paper_id:
            return {
                "title": paper["title"],
                "current_citations": paper.get("citations", 0),
                "last_updated": datetime.now().isoformat()
            }
    
    return None
```

## Available Endpoints

| Endpoint | Description | Update Frequency |
|----------|-------------|------------------|
| `/data/papers_latest.json` | All papers with metadata | Daily |
| `/data/stats.json` | Collection statistics | Daily |
| `/docs/dashboard.html` | Interactive visualization | Daily |
| `/README.md` | Formatted paper list | Daily |
| `/SURVEY.md` | AI-generated survey | Weekly |

## License

The data is provided under the same license as the repository. Please cite this repository if you use the data in your research:

```bibtex
@misc{awesome-genai-healthcare,
  title={Awesome Generative AI in Healthcare Papers},
  author={GitHub Community},
  year={2025},
  url={https://github.com/dingyucanada/Awesome-GenAI-Healthcare}
}
```

## Support

For issues or feature requests:
- Open an issue on [GitHub](https://github.com/dingyucanada/Awesome-GenAI-Healthcare/issues)
- See [Contributing Guidelines](CONTRIBUTING.md)

---
*Last updated: 2025-09-02*