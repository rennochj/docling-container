#!/usr/bin/env bash
# Build multi-platform Docker images

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
echo "📦 Building version: $VERSION"

# Parse version components
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Ensure builder exists
if ! docker buildx inspect "$BUILDER_NAME" &> /dev/null; then
    echo "⚠️  Builder '$BUILDER_NAME' not found, creating..."
    ./scripts/setup-buildx.sh
fi

# Use the multi-platform builder
docker buildx use "$BUILDER_NAME"

echo ""
echo "🏗️  Building multi-platform images for:"
echo "   Platforms: $PLATFORMS"
echo "   Version: $VERSION"
echo ""

# Build and load for local testing (single platform)
echo "Building for local platform (testing)..."
docker buildx build \
    --platform "$(docker version --format '{{.Server.Os}}/{{.Server.Arch}}')" \
    --tag "${IMAGE_NAME}:${VERSION}" \
    --tag "${IMAGE_NAME}:${MAJOR}.${MINOR}" \
    --tag "${IMAGE_NAME}:${MAJOR}" \
    --tag "${IMAGE_NAME}:latest" \
    --load \
    .

echo ""
echo "✓ Local build complete!"
echo ""
echo "Building for all platforms (will be pushed separately)..."

# Build for all platforms (creates manifest, but doesn't push)
docker buildx build \
    --platform "$PLATFORMS" \
    --tag "${IMAGE_NAME}:${VERSION}" \
    --tag "${IMAGE_NAME}:${MAJOR}.${MINOR}" \
    --tag "${IMAGE_NAME}:${MAJOR}" \
    --tag "${IMAGE_NAME}:latest" \
    .

echo ""
echo "✓ Multi-platform build complete!"
echo ""
echo "Built images with tags:"
echo "  - ${IMAGE_NAME}:${VERSION}"
echo "  - ${IMAGE_NAME}:${MAJOR}.${MINOR}"
echo "  - ${IMAGE_NAME}:${MAJOR}"
echo "  - ${IMAGE_NAME}:latest"
