#!/usr/bin/env bash
# Setup Docker Buildx for multi-platform builds

set -e

BUILDER_NAME="docling-multiplatform"

echo "🔧 Setting up Docker Buildx for multi-platform builds..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    exit 1
fi

# Check if buildx is available
if ! docker buildx version &> /dev/null; then
    echo "❌ Error: Docker Buildx is not available"
    echo "   Please update Docker to a version that includes Buildx"
    exit 1
fi

# Check if builder already exists
if docker buildx inspect "$BUILDER_NAME" &> /dev/null; then
    echo "✓ Builder '$BUILDER_NAME' already exists"
    docker buildx use "$BUILDER_NAME"
else
    echo "Creating new builder '$BUILDER_NAME'..."
    docker buildx create --name "$BUILDER_NAME" --driver docker-container --bootstrap --use
    echo "✓ Builder created successfully"
fi

# Verify the builder supports required platforms
echo ""
echo "Supported platforms:"
docker buildx inspect --bootstrap | grep "Platforms:"

echo ""
echo "✓ Buildx setup complete!"
