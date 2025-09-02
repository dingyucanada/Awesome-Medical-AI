#!/bin/bash

# Setup script for Awesome Healthcare AI Papers
echo "🏥 Setting up Awesome Healthcare AI Papers..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install requests matplotlib pandas

# Create data directories
echo "Creating necessary directories..."
mkdir -p data
mkdir -p docs/images

# Run initial paper collection
echo "Running initial paper collection..."
python3 scripts/collect_papers.py

# Update README
echo "Updating README..."
python3 scripts/update_readme.py

# Generate survey
echo "Generating initial survey..."
python3 scripts/generate_survey.py

# Generate visualizations
echo "Generating visualizations..."
python3 scripts/generate_viz.py

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a GitHub repository"
echo "2. Push this project to GitHub"
echo "3. Add OPENAI_API_KEY to repository secrets (optional, for better surveys)"
echo "4. GitHub Actions will automatically update daily"
echo ""
echo "Manual commands:"
echo "  python3 scripts/collect_papers.py  # Collect new papers"
echo "  python3 scripts/update_readme.py   # Update README"
echo "  python3 scripts/generate_survey.py # Generate survey"
echo "  python3 scripts/generate_viz.py    # Generate visualizations"