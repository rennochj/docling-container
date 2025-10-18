#!/usr/bin/env bash
# Push multi-platform images to GitHub Container Registry (GHCR)

set -e

# Configuration
BUILDER_NAME="docling-multiplatform"
IMAGE_NAME="ghcr.io/rennochj/docling-container"
PLATFORMS="linux/amd64,linux/arm64"

# Read version from VERSION file
if [ ! -f "VERSION" ]; then
    echo "❌ Error: VERSION file not found"
    exit 1
fi

VERSION=$(cat VERSION)
echo "📦 Pushing version: $VERSION"

# Parse version components
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Check if logged in to GHCR
echo "🔐 Checking GHCR authentication..."

# Check if already authenticated by looking at Docker config
if grep -q "ghcr.io" ~/.docker/config.json 2>/dev/null; then
    echo "✓ Already authenticated to GHCR"
elif [ -n "$GITHUB_TOKEN" ]; then
    echo "Authenticating with GITHUB_TOKEN..."
    if echo "$GITHUB_TOKEN" | docker login ghcr.io -u rennochj --password-stdin 2>/dev/null; then
        echo "✓ Authenticated to GHCR"
    else
        echo "❌ Failed to authenticate with GITHUB_TOKEN"
        exit 1
    fi
else
    echo "⚠️  Not logged in to GHCR and GITHUB_TOKEN not set."
    echo ""
    echo "Please authenticate using one of these methods:"
    echo ""
    echo "  1. Login directly:"
    echo "     docker login ghcr.io -u rennochj"
    echo ""
    echo "  2. Or use a GitHub Personal Access Token:"
    echo "     export GITHUB_TOKEN=your_token_here"
    echo "     echo \$GITHUB_TOKEN | docker login ghcr.io -u rennochj --password-stdin"
    echo ""
    exit 1
fi

# Ensure builder exists
if ! docker buildx inspect "$BUILDER_NAME" &> /dev/null; then
    echo "❌ Error: Builder '$BUILDER_NAME' not found"
    echo "   Run './scripts/setup-buildx.sh' first"
    exit 1
fi

# Use the multi-platform builder
docker buildx use "$BUILDER_NAME"

echo ""
echo "🚀 Pushing multi-platform images to GHCR..."
echo "   Platforms: $PLATFORMS"
echo "   Version: $VERSION"
echo ""

# Build and push all platforms with all tags
docker buildx build \
    --platform "$PLATFORMS" \
    --tag "${IMAGE_NAME}:${VERSION}" \
    --tag "${IMAGE_NAME}:${MAJOR}.${MINOR}" \
    --tag "${IMAGE_NAME}:${MAJOR}" \
    --tag "${IMAGE_NAME}:latest" \
    --push \
    .

echo ""
echo "✅ Successfully pushed to GHCR!"
echo ""
echo "Published images:"
echo "  🔗 ${IMAGE_NAME}:${VERSION}"
echo "  🔗 ${IMAGE_NAME}:${MAJOR}.${MINOR}"
echo "  🔗 ${IMAGE_NAME}:${MAJOR}"
echo "  🔗 ${IMAGE_NAME}:latest"
echo ""
echo "Users can pull with:"
echo "  docker pull ${IMAGE_NAME}:${VERSION}"
echo "  docker pull ${IMAGE_NAME}:latest"
