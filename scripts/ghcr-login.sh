#!/usr/bin/env bash
# Login to GitHub Container Registry with PAT token

set -e

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable is not set"
    echo ""
    echo "Please set your GitHub Personal Access Token:"
    echo "  export GITHUB_TOKEN=ghp_your_token_here"
    exit 1
fi

echo "🔐 Logging in to GitHub Container Registry..."
echo "   Username: rennochj"

# Use printf to avoid TTY issues
printf '%s' "$GITHUB_TOKEN" | docker login ghcr.io -u rennochj --password-stdin

echo ""
echo "✅ Successfully logged in to ghcr.io"
echo ""
echo "You can now run:"
echo "  make push-ghcr"
