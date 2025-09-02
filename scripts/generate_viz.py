#!/usr/bin/env python3
"""
Generate visualizations for the paper collection
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import base64
from io import BytesIO

# Try to import visualization libraries
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import pandas as pd
    HAS_VIZ = True
except ImportError:
    HAS_VIZ = False
    print("Warning: matplotlib/pandas not installed. Visualizations will be skipped.")

class VizGenerator:
    def __init__(self):
        self.project_dir = Path(__file__).parent.parent
        self.data_dir = self.project_dir / "data"
        self.viz_dir = self.project_dir / "docs" / "images"
        self.viz_dir.mkdir(parents=True, exist_ok=True)
        
    def load_papers(self) -> List[Dict]:
        """Load papers from latest JSON file"""
        latest_filepath = self.data_dir / "papers_latest.json"
        if latest_filepath.exists():
            with open(latest_filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def generate_html_dashboard(self, papers: List[Dict]) -> str:
        """Generate HTML dashboard without matplotlib"""
        # Basic statistics
        stats = self.calculate_stats(papers)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Healthcare AI Papers Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                  gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 10px; 
                      box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        .chart {{ background: white; padding: 20px; border-radius: 10px; 
                  margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .bar {{ background: #667eea; height: 30px; margin: 5px 0; 
                border-radius: 5px; position: relative; }}
        .bar-label {{ position: absolute; left: 10px; line-height: 30px; color: white; }}
        .bar-value {{ position: absolute; right: 10px; line-height: 30px; color: white; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #667eea; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .trend {{ display: inline-block; padding: 5px 10px; margin: 5px; 
                  background: #e0e7ff; color: #667eea; border-radius: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Healthcare AI Papers Dashboard</h1>
            <p>Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{stats['total']}</div>
                <div class="stat-label">Total Papers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['last_week']}</div>
                <div class="stat-label">Last 7 Days</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['last_month']}</div>
                <div class="stat-label">Last 30 Days</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(stats['categories'])}</div>
                <div class="stat-label">Categories</div>
            </div>
        </div>
        
        <div class="chart">
            <h2>📊 Papers by Category</h2>
            {self.generate_bar_chart_html(stats['categories'])}
        </div>
        
        <div class="chart">
            <h2>📈 Monthly Trend</h2>
            {self.generate_trend_html(stats['monthly'])}
        </div>
        
        <div class="chart">
            <h2>🔥 Trending Topics</h2>
            <div>
                {''.join([f'<span class="trend">{topic}</span>' for topic in stats['trending']])}
            </div>
        </div>
        
        <div class="chart">
            <h2>📚 Recent Papers</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Title</th>
                    <th>Category</th>
                    <th>Source</th>
                </tr>
                {''.join([f'''<tr>
                    <td>{p.get('published', '')[:10]}</td>
                    <td>{p.get('title', '')[:80]}...</td>
                    <td>{p.get('category', '')}</td>
                    <td>{p.get('source', '')}</td>
                </tr>''' for p in papers[:10]])}
            </table>
        </div>
    </div>
</body>
</html>"""
        return html
    
    def generate_bar_chart_html(self, data: Dict) -> str:
        """Generate HTML bar chart"""
        if not data:
            return "<p>No data available</p>"
        
        max_value = max(data.values())
        html = ""
        
        for category, count in sorted(data.items(), key=lambda x: x[1], reverse=True):
            width = (count / max_value * 100) if max_value > 0 else 0
            html += f'''<div style="margin: 10px 0;">
                <div style="display: flex; align-items: center;">
                    <div style="width: 150px; text-align: right; padding-right: 10px;">{category}</div>
                    <div style="flex: 1; background: #e0e7ff; border-radius: 5px;">
                        <div class="bar" style="width: {width}%;">
                            <span class="bar-value">{count}</span>
                        </div>
                    </div>
                </div>
            </div>'''
        
        return html
    
    def generate_trend_html(self, data: Dict) -> str:
        """Generate trend visualization in HTML"""
        if not data:
            return "<p>No trend data available</p>"
        
        html = '<div style="display: flex; justify-content: space-around; flex-wrap: wrap;">'
        
        for month, count in sorted(data.items())[-6:]:  # Last 6 months
            html += f'''<div style="text-align: center; margin: 10px;">
                <div style="background: #667eea; color: white; width: 60px; height: {min(count*10, 200)}px; 
                            margin: 0 auto; border-radius: 5px; display: flex; align-items: flex-end; 
                            justify-content: center; padding: 10px;">
                    <span>{count}</span>
                </div>
                <div style="margin-top: 5px; font-size: 0.9em;">{month}</div>
            </div>'''
        
        html += '</div>'
        return html
    
    def calculate_stats(self, papers: List[Dict]) -> Dict:
        """Calculate statistics from papers"""
        stats = {
            'total': len(papers),
            'last_week': 0,
            'last_month': 0,
            'categories': {},
            'monthly': {},
            'sources': {},
            'trending': []
        }
        
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        for paper in papers:
            # Parse date
            try:
                pub_date = datetime.strptime(paper.get('published', '')[:10], '%Y-%m-%d')
                
                if pub_date >= week_ago:
                    stats['last_week'] += 1
                if pub_date >= month_ago:
                    stats['last_month'] += 1
                
                # Monthly stats
                month_key = pub_date.strftime('%Y-%m')
                stats['monthly'][month_key] = stats['monthly'].get(month_key, 0) + 1
                
            except:
                pass
            
            # Category stats
            category = paper.get('category', 'unknown')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            # Source stats
            source = paper.get('source', 'unknown')
            stats['sources'][source] = stats['sources'].get(source, 0) + 1
        
        # Trending topics (simplified)
        stats['trending'] = ['LLM', 'Clinical AI', 'Medical Imaging', 'Drug Discovery', 
                            'Federated Learning', 'Multimodal Models']
        
        return stats
    
    def generate_matplotlib_charts(self, papers: List[Dict]):
        """Generate charts using matplotlib if available"""
        if not HAS_VIZ:
            return
        
        stats = self.calculate_stats(papers)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Healthcare AI Papers Analytics', fontsize=16, fontweight='bold')
        
        # 1. Papers by Category
        ax1 = axes[0, 0]
        categories = list(stats['categories'].keys())
        counts = list(stats['categories'].values())
        ax1.barh(categories, counts, color='#667eea')
        ax1.set_xlabel('Number of Papers')
        ax1.set_title('Papers by Category')
        ax1.grid(True, alpha=0.3)
        
        # 2. Monthly Trend
        ax2 = axes[0, 1]
        months = sorted(stats['monthly'].keys())[-12:]  # Last 12 months
        monthly_counts = [stats['monthly'].get(m, 0) for m in months]
        ax2.plot(range(len(months)), monthly_counts, marker='o', linewidth=2, 
                markersize=8, color='#764ba2')
        ax2.set_xticks(range(len(months)))
        ax2.set_xticklabels([m[-2:] + '/' + m[2:4] for m in months], rotation=45)
        ax2.set_ylabel('Number of Papers')
        ax2.set_title('Monthly Publication Trend')
        ax2.grid(True, alpha=0.3)
        
        # 3. Source Distribution
        ax3 = axes[1, 0]
        sources = list(stats['sources'].keys())
        source_counts = list(stats['sources'].values())
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']
        ax3.pie(source_counts, labels=sources, autopct='%1.1f%%', colors=colors)
        ax3.set_title('Papers by Source')
        
        # 4. Recent Activity Heatmap
        ax4 = axes[1, 1]
        # Create a simple activity matrix (last 4 weeks x 7 days)
        activity = [[0 for _ in range(7)] for _ in range(4)]
        for paper in papers:
            try:
                pub_date = datetime.strptime(paper.get('published', '')[:10], '%Y-%m-%d')
                days_ago = (datetime.now() - pub_date).days
                if days_ago < 28:
                    week = days_ago // 7
                    day = days_ago % 7
                    activity[week][day] += 1
            except:
                pass
        
        im = ax4.imshow(activity, cmap='YlOrRd', aspect='auto')
        ax4.set_xticks(range(7))
        ax4.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        ax4.set_yticks(range(4))
        ax4.set_yticklabels(['This Week', '1 Week Ago', '2 Weeks Ago', '3 Weeks Ago'])
        ax4.set_title('Publication Activity Heatmap')
        plt.colorbar(im, ax=ax4)
        
        plt.tight_layout()
        
        # Save figure
        chart_path = self.viz_dir / 'dashboard.png'
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Charts saved to {chart_path}")
    
    def generate_all(self):
        """Generate all visualizations"""
        print("Generating visualizations...")
        
        # Load papers
        papers = self.load_papers()
        if not papers:
            print("No papers found. Run collect_papers.py first.")
            return
        
        # Generate HTML dashboard
        html_content = self.generate_html_dashboard(papers)
        dashboard_path = self.project_dir / "docs" / "dashboard.html"
        dashboard_path.parent.mkdir(exist_ok=True)
        
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"HTML dashboard saved to {dashboard_path}")
        
        # Generate matplotlib charts if available
        if HAS_VIZ:
            self.generate_matplotlib_charts(papers)
        
        # Update README with dashboard link
        readme_path = self.project_dir / "README.md"
        if readme_path.exists():
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "dashboard.html" not in content:
                # Add dashboard link after the trends section
                dashboard_section = "\n### 📊 [Interactive Dashboard](docs/dashboard.html)\n"
                content = content.replace("### Monthly Statistics", 
                                        dashboard_section + "\n### Monthly Statistics")
                
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(content)
        
        print("Visualization generation complete!")

if __name__ == "__main__":
    generator = VizGenerator()
    generator.generate_all()