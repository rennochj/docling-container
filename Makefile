# Makefile for docling-container
# Common operations for building and running the Docling document conversion container

# Variables
IMAGE_NAME := docling-container
IMAGE_TAG := latest
FULL_IMAGE := $(IMAGE_NAME):$(IMAGE_TAG)
INPUT_DIR := $(PWD)/examples
OUTPUT_DIR := $(PWD)/output
DOCKER_RUN := docker run --rm -v $(INPUT_DIR):/input -v $(OUTPUT_DIR):/output $(FULL_IMAGE)

# Default target
.DEFAULT_GOAL := help

# PHONY targets (not files)
.PHONY: help build clean clean-output clean-images setup run-html run-md run-batch run-all shell test \
        version show-version release-patch release-minor release-major \
        build-multiplatform push-ghcr setup-buildx changelog

##@ General

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup

setup: ## Create required directories
	@echo "Creating directories..."
	@mkdir -p $(INPUT_DIR)
	@mkdir -p $(OUTPUT_DIR)
	@echo "Directories created: examples/ and output/"

##@ Build

build: ## Build the Docker image
	@echo "Building Docker image: $(FULL_IMAGE)..."
	docker build -t $(FULL_IMAGE) .
	@echo "Build complete!"

rebuild: clean-images build ## Clean and rebuild the Docker image

##@ Clean

clean: clean-output clean-images ## Clean output files and Docker images

clean-output: ## Remove all files from output directory
	@echo "Cleaning output directory..."
	@rm -rf $(OUTPUT_DIR)/*
	@echo "Output directory cleaned!"

clean-images: ## Remove Docker image
	@echo "Removing Docker image: $(FULL_IMAGE)..."
	@docker rmi $(FULL_IMAGE) 2>/dev/null || true
	@echo "Docker image removed!"

##@ Run Examples

run-html: ## Convert sample.html to markdown
	@echo "Converting sample.html to markdown..."
	$(DOCKER_RUN) convert /input/sample.html /output -f markdown

run-md: ## Convert sample.md to HTML
	@echo "Converting sample.md to HTML..."
	$(DOCKER_RUN) convert /input/sample.md /output -f html

run-html-json: ## Convert sample.html to JSON
	@echo "Converting sample.html to JSON..."
	$(DOCKER_RUN) convert /input/sample.html /output -f json

run-pptx: ## Convert architecture-example.pptx to markdown
	@echo "Converting architecture-example.pptx to markdown..."
	$(DOCKER_RUN) convert /input/architecture-example.pptx /output -f markdown

run-pdf: ## Convert file-example_PDF_1MB.pdf to markdown
	@echo "Converting file-example_PDF_1MB.pdf to markdown..."
	$(DOCKER_RUN) convert file-example_PDF_1MB.pdf /output -f markdown

run-url: ## Convert https://arxiv.org/pdf/2408.09869 to markdown
	@echo "Converting https://arxiv.org/pdf/2408.09869 to markdown..."
	$(DOCKER_RUN) convert https://arxiv.org/pdf/2408.09869 /output -f markdown

run-batch: ## Run batch conversion on all files in examples/
	@echo "Running batch conversion on all files in examples/..."
	$(DOCKER_RUN) convert --batch -f markdown

run-batch-html: ## Run batch conversion to HTML format
	@echo "Running batch conversion to HTML..."
	$(DOCKER_RUN) convert --batch -f html

run-all: run-html run-md run-html-json ## Run all individual example conversions

##@ Image Extraction Examples

run-pptx-images: ## Convert architecture-example.pptx to markdown
	@echo "Converting architecture-example.pptx to markdown..."
	$(DOCKER_RUN) convert /input/architecture-example.pptx /output -f markdown --export-images

run-pdf-images: ## Convert PDF and extract images
	@echo "Converting file-example_PDF_1MB.pdf with image extraction..."
	$(DOCKER_RUN) convert file-example_PDF_1MB.pdf /output -f markdown --export-images

run-url-images: ## Convert URL and extract images
	@echo "Converting https://arxiv.org/pdf/2408.09869 with image extraction..."
	$(DOCKER_RUN) convert https://arxiv.org/pdf/2408.09869 /output -f markdown --export-images

run-images-hires: ## Convert PDF with high-resolution images (4x scale)
	@echo "Converting file-example_PDF_1MB.pdf with high-res images..."
	$(DOCKER_RUN) convert file-example_PDF_1MB.pdf /output -f markdown --export-images --images-scale 4.0

run-images-with-pages: ## Convert PDF and extract ALL images including page renders
	@echo "Converting file-example_PDF_1MB.pdf with all images (including pages)..."
	$(DOCKER_RUN) convert file-example_PDF_1MB.pdf /output -f markdown --export-images --export-page-images

##@ Development

shell: ## Open a shell in the container
	docker run --rm -it -v $(INPUT_DIR):/input -v $(OUTPUT_DIR):/output --entrypoint /bin/bash $(FULL_IMAGE)

logs: ## View most recent container logs
	docker logs $$(docker ps -lq)

inspect: ## Show Docker image details
	docker inspect $(FULL_IMAGE)

##@ Testing

test-local: ## Run tests locally with uv
	@echo "Running tests locally..."
	uv run pytest tests/ -v

test-docker: build ## Run tests inside Docker container
	@echo "Running tests in Docker container..."
	docker run --rm $(FULL_IMAGE) python -m pytest tests/ -v

##@ Utilities

show-output: ## Display contents of output directory
	@echo "Contents of output/:"
	@ls -lh $(OUTPUT_DIR)

show-examples: ## Display contents of examples directory
	@echo "Contents of examples/:"
	@ls -lh $(INPUT_DIR)

validate: ## Validate Dockerfile syntax
	@echo "Validating Dockerfile..."
	docker build --check .

version: ## Show Docker and tool versions
	@echo "Docker version:"
	@docker --version
	@echo "\nPython version in container:"
	@docker run --rm $(FULL_IMAGE) python --version 2>/dev/null || echo "Image not built yet"
	@echo "\nLocal uv version:"
	@uv --version 2>/dev/null || echo "uv not installed locally"

##@ Versioning & Release

show-version: ## Show current version
	@echo "Current version: $$(cat VERSION)"
	@echo "Git tags:"
	@git tag -l | tail -5 || echo "  No tags yet"

changelog: ## Generate CHANGELOG.md from conventional commits
	@echo "Generating changelog..."
	@git-cliff --output CHANGELOG.md || echo "⚠️  git-cliff not installed. Install with: brew install git-cliff"

setup-buildx: ## Setup Docker Buildx for multi-platform builds
	@./scripts/setup-buildx.sh

build-multiplatform: ## Build multi-platform images (amd64 + arm64)
	@./scripts/build-multiplatform.sh

push-ghcr: ## Push images to GitHub Container Registry
	@./scripts/push-ghcr.sh

release-patch: ## Create a patch release (0.1.0 -> 0.1.1)
	@./scripts/release.sh patch

release-minor: ## Create a minor release (0.1.0 -> 0.2.0)
	@./scripts/release.sh minor

release-major: ## Create a major release (0.1.0 -> 1.0.0)
	@./scripts/release.sh major

##@ Quick Start

quick-start: setup build run-batch show-output ## Setup, build, and run batch conversion
	@echo "\n✓ Quick start complete! Check output/ for converted files."
