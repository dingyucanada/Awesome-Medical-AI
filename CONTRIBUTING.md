# 🤝 Contributing Guidelines

Thank you for your interest in contributing to Awesome Generative AI in Healthcare Papers! This repository thrives on community contributions.

## How to Contribute

### 🐛 Report Issues

Found a problem? Please help us improve:

1. **Check existing issues** first to avoid duplicates
2. **Create a new issue** with a clear title
3. **Describe the problem** in detail:
   - What you expected to happen
   - What actually happened
   - Steps to reproduce

[Report an Issue →](https://github.com/dingyucanada/Awesome-GenAI-Healthcare/issues/new)

### 📝 Suggest Papers

Know a great paper we're missing? 

#### Option 1: Open an Issue
Create an issue with the `paper-suggestion` label including:
- Paper title
- Authors
- Publication venue/date
- ArXiv ID or PubMed ID
- Why it's relevant to Healthcare AI

#### Option 2: Submit a Pull Request
Add the paper directly to `data/papers_latest.json`:

```json
{
  "title": "Your Paper Title",
  "authors": ["Author 1", "Author 2"],
  "published": "2025-MM-DD",
  "source": "arxiv",
  "arxiv_id": "2501.00000",
  "category": "clinical_apps",
  "abstract": "Paper abstract...",
  "pdf_url": "https://...",
  "citations": 0
}
```

### 💡 Improve Classification

Help us better categorize papers:

1. Review papers in the "foundation" category
2. Suggest more specific categories
3. Propose new category definitions

### 🔧 Fix Metadata

Found incorrect information?

- Wrong links
- Missing PMIDs
- Incorrect citations
- Wrong categories

Submit a PR with corrections to `data/papers_latest.json`

### 🌟 Add Features

Want to add new functionality?

1. **Discuss first**: Open an issue describing your idea
2. **Fork the repository**
3. **Create a feature branch**: `git checkout -b feature/amazing-feature`
4. **Make your changes**
5. **Test thoroughly**
6. **Submit a Pull Request**

## Code Contributions

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/dingyucanada/Awesome-GenAI-Healthcare.git
cd Awesome-GenAI-Healthcare

# Install dependencies
pip install -r requirements.txt

# Run tests
python scripts/collect_papers.py
python scripts/update_readme.py
```

### Code Style

- Python: Follow PEP 8
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

### Testing

Before submitting:

1. Run paper collection script
2. Verify README updates correctly
3. Check that all links work
4. Ensure JSON is valid

```bash
# Test paper collection
python scripts/collect_papers.py

# Validate JSON
python -m json.tool data/papers_latest.json > /dev/null

# Update README
python scripts/update_readme.py
```

## Pull Request Process

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### PR Checklist

- [ ] Descriptive title and description
- [ ] Links to related issues
- [ ] No broken links
- [ ] JSON validates successfully
- [ ] Categories are appropriate
- [ ] No duplicate papers

## Paper Selection Criteria

Papers should meet these criteria:

### ✅ Include

- Direct applications of generative AI in healthcare
- LLMs for clinical tasks
- Medical image generation/synthesis
- Drug discovery using generative models
- Clinical documentation automation
- Patient interaction systems
- Healthcare-specific model architectures
- Ethics and safety in medical AI

### ❌ Exclude

- General AI papers without healthcare focus
- Pure diagnostic AI (non-generative)
- Traditional ML in healthcare
- Papers without clear healthcare application

## Community Guidelines

### Be Respectful
- Welcome newcomers
- Provide constructive feedback
- Respect different viewpoints

### Be Helpful
- Answer questions when you can
- Share your expertise
- Guide others to resources

### Be Professional
- Keep discussions focused
- Avoid off-topic conversations
- Maintain academic standards

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Special mentions in major updates
- Annual contributor summary

## Questions?

- Open a [Discussion](https://github.com/dingyucanada/Awesome-GenAI-Healthcare/discussions)
- Check our [FAQ](#frequently-asked-questions)
- Review [API Documentation](docs/API.md)

## Frequently Asked Questions

### Q: How often is the collection updated?
A: Daily at 00:00 UTC via GitHub Actions

### Q: Can I add papers from other sources?
A: Yes! We welcome papers from any reputable source

### Q: How are categories determined?
A: Combination of keyword matching and ML classification

### Q: Can I use this data for research?
A: Yes! Please cite the repository in your work

### Q: How can I get notified of updates?
A: Watch the repository or star it for updates

## License

By contributing, you agree that your contributions will be licensed under the same license as this repository.

## Contact

- GitHub Issues: [Report problems](https://github.com/dingyucanada/Awesome-GenAI-Healthcare/issues)
- Discussions: [Ask questions](https://github.com/dingyucanada/Awesome-GenAI-Healthcare/discussions)

---

Thank you for helping make this resource better for everyone! 🙏

*Last updated: 2025-09-02*