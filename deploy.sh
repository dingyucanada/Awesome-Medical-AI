#!/bin/bash

echo "🚀 Automated GitHub Deployment Script"
echo "======================================"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI (gh) not found. Installing..."
    
    # Check OS and install gh
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install gh
        else
            echo "❌ Please install Homebrew first: https://brew.sh"
            echo "Then run: brew install gh"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install gh
    else
        echo "❌ Unsupported OS. Please install GitHub CLI manually: https://cli.github.com/"
        exit 1
    fi
fi

# Authenticate with GitHub
echo "📝 Please authenticate with GitHub..."
echo "You'll be redirected to your browser to complete authentication."
echo ""
gh auth login --web

# Create repository
echo ""
echo "📦 Creating GitHub repository..."
REPO_NAME="Awesome-GenAI-Healthcare"

# Check if repo already exists
if gh repo view $REPO_NAME &> /dev/null; then
    echo "⚠️  Repository '$REPO_NAME' already exists."
    read -p "Do you want to use the existing repository? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter a new repository name: " REPO_NAME
    fi
fi

# Create the repository
gh repo create $REPO_NAME --public --description "🏥 Auto-updating collection of Generative AI in Healthcare papers with AI-powered surveys" --confirm

# Get the repository URL
REPO_URL=$(gh repo view $REPO_NAME --json url -q .url)
echo "✅ Repository created: $REPO_URL"

# Add remote and push
echo ""
echo "📤 Pushing code to GitHub..."
git remote remove origin 2>/dev/null  # Remove if exists
git remote add origin $REPO_URL.git
git branch -M main
git push -u origin main

# Enable GitHub Actions
echo ""
echo "⚙️  Configuring GitHub Actions..."
gh api repos/$(gh api user -q .login)/$REPO_NAME/actions/permissions \
  --method PUT \
  -f enabled=true \
  -f allowed_actions=all

# Set workflow permissions
gh api repos/$(gh api user -q .login)/$REPO_NAME/actions/permissions/workflow \
  --method PUT \
  -f default_workflow_permissions=write \
  -f can_approve_pull_request_reviews=true

echo "✅ GitHub Actions enabled with write permissions"

# Optional: Add OpenAI API Key
echo ""
echo "🤖 Optional: Add OpenAI API Key for better AI summaries"
read -p "Do you have an OpenAI API key to add? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -sp "Enter your OpenAI API key: " OPENAI_KEY
    echo
    gh secret set OPENAI_API_KEY --body="$OPENAI_KEY" --repo=$REPO_NAME
    echo "✅ OpenAI API key added successfully"
fi

# Trigger first workflow run
echo ""
echo "🎯 Triggering first workflow run..."
gh workflow run "Daily Paper Update" --repo=$REPO_NAME

echo ""
echo "🎉 Deployment Complete!"
echo "========================"
echo ""
echo "📊 Your repository is live at: $REPO_URL"
echo "⚡ GitHub Actions will update daily at 00:00 UTC"
echo "📈 Check the Actions tab to see the workflow progress"
echo ""
echo "Next steps:"
echo "1. Visit $REPO_URL"
echo "2. Star ⭐ your repository"
echo "3. Check Actions tab for the first run"
echo "4. View the dashboard at: $REPO_URL/blob/main/docs/dashboard.html"
echo ""
echo "Manual update command:"
echo "  gh workflow run 'Daily Paper Update' --repo=$REPO_NAME"