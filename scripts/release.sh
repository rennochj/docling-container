#!/usr/bin/env bash
# Automated release script for docling-forge
# Handles versioning, building, pushing, and GitHub release creation

set -e

# Colors for output (using ANSI-C quoting for proper escape sequence interpretation)
RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
NC=$'\033[0m' # No Color

# Configuration
GITHUB_REPO="rennochj/docling-forge"
IMAGE_NAME="ghcr.io/${GITHUB_REPO}"

# Helper functions
print_header() {
    echo ""
    printf "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
    printf "${BLUE}  %s${NC}\n" "$1"
    printf "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
    echo ""
}

print_success() {
    printf "${GREEN}✓${NC} %s\n" "$1"
}

print_error() {
    printf "${RED}✗${NC} %s\n" "$1"
}

print_warning() {
    printf "${YELLOW}⚠${NC} %s\n" "$1"
}

print_info() {
    printf "${BLUE}ℹ${NC} %s\n" "$1"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    local missing=0

    # Check for required tools
    for tool in git docker bump2version gh; do
        if command -v "$tool" &> /dev/null; then
            print_success "$tool installed"
        else
            print_error "$tool not found"
            missing=1
        fi
    done

    # Check for git-cliff (optional but recommended)
    if command -v git-cliff &> /dev/null; then
        print_success "git-cliff installed"
    else
        print_warning "git-cliff not found (changelog generation will be skipped)"
        print_info "Install with: cargo install git-cliff OR brew install git-cliff"
    fi

    # Check Docker Buildx
    if docker buildx version &> /dev/null; then
        print_success "Docker Buildx available"
    else
        print_error "Docker Buildx not available"
        missing=1
    fi

    # Check gh authentication
    if gh auth status &> /dev/null; then
        print_success "GitHub CLI authenticated"
    else
        print_error "GitHub CLI not authenticated"
        print_info "Run: gh auth login"
        missing=1
    fi

    if [ $missing -eq 1 ]; then
        print_error "Missing required tools. Please install them and try again."
        exit 1
    fi
}

# Validate git status
validate_git_status() {
    print_header "Validating Git Status"

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi

    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_error "You have uncommitted changes. Please commit or stash them first."
        git status --short
        exit 1
    fi

    print_success "Working directory is clean"

    # Check if we're on master/main branch
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "master" ] && [ "$CURRENT_BRANCH" != "main" ]; then
        print_warning "You are on branch '$CURRENT_BRANCH', not master/main"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    print_success "On branch: $CURRENT_BRANCH"
}

# Bump version
bump_version() {
    local bump_type=$1

    print_header "Bumping Version ($bump_type)"

    # Get current version
    CURRENT_VERSION=$(cat VERSION)
    print_info "Current version: $CURRENT_VERSION"

    # Bump version
    bump2version --allow-dirty "$bump_type"

    # Get new version
    NEW_VERSION=$(cat VERSION)
    print_success "New version: $NEW_VERSION"

    export VERSION=$NEW_VERSION
}

# Generate changelog
generate_changelog() {
    print_header "Generating Changelog"

    if ! command -v git-cliff &> /dev/null; then
        print_warning "git-cliff not installed, skipping changelog generation"
        return
    fi

    # Generate changelog
    git-cliff --output CHANGELOG.md

    print_success "Changelog generated: CHANGELOG.md"
}

# Run tests
run_tests() {
    print_header "Running Tests"

    if [ -f "pyproject.toml" ] && command -v uv &> /dev/null; then
        print_info "Running pytest..."
        if uv run pytest tests/ -v; then
            print_success "All tests passed"
        else
            print_error "Tests failed"
            exit 1
        fi
    else
        print_warning "Skipping tests (uv or pyproject.toml not found)"
    fi
}

# Build multi-platform images
build_images() {
    print_header "Building Multi-Platform Images"

    ./scripts/setup-buildx.sh
    ./scripts/build-multiplatform.sh

    print_success "Images built successfully"
}

# Push to GHCR
push_images() {
    print_header "Pushing Images to GHCR"

    ./scripts/push-ghcr.sh

    print_success "Images pushed successfully"
}

# Commit and tag
commit_and_tag() {
    print_header "Committing and Tagging"

    # Add changed files
    git add VERSION pyproject.toml .bumpversion.cfg

    if [ -f "CHANGELOG.md" ]; then
        git add CHANGELOG.md
    fi

    # Check if there are changes to commit
    if git diff-index --quiet HEAD --; then
        print_warning "No changes to commit (already committed)"
    else
        # Commit
        git commit -m "chore(release): prepare for v${VERSION}

- Bump version to ${VERSION}
- Update changelog

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

        print_success "Changes committed"
    fi

    # Check if tag already exists
    if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
        print_warning "Tag v${VERSION} already exists, skipping tag creation"
    else
        # Create git tag
        git tag -a "v${VERSION}" -m "Release v${VERSION}"
        print_success "Tag created: v${VERSION}"
    fi
}

# Push to GitHub
push_to_github() {
    print_header "Pushing to GitHub"

    # Push commits
    if git push origin $(git branch --show-current); then
        print_success "Commits pushed to GitHub"
    else
        print_warning "No new commits to push (already up to date)"
    fi

    # Push tag
    if git push origin "v${VERSION}" 2>&1 | grep -q "up-to-date"; then
        print_warning "Tag v${VERSION} already pushed"
    else
        print_success "Tag v${VERSION} pushed to GitHub"
    fi
}

# Create GitHub release
create_github_release() {
    print_header "Creating GitHub Release"

    # Check if release already exists
    if gh release view "v${VERSION}" &> /dev/null; then
        print_warning "GitHub release v${VERSION} already exists, skipping"
        return
    fi

    # Extract changelog for this version
    local release_notes=""
    if [ -f "CHANGELOG.md" ] && command -v git-cliff &> /dev/null; then
        # Get changelog section for this version
        release_notes=$(git-cliff --unreleased --strip header)
    else
        release_notes="Release v${VERSION}"
    fi

    # Create release
    if echo "$release_notes" | gh release create "v${VERSION}" \
        --title "v${VERSION}" \
        --notes-file -; then
        print_success "GitHub release created"
    else
        print_error "Failed to create GitHub release"
        exit 1
    fi
}

# Display summary
display_summary() {
    print_header "Release Summary"

    printf "${GREEN}🎉 Release v${VERSION} completed successfully!${NC}\n"
    echo ""
    printf "Released version: ${GREEN}v${VERSION}${NC}\n"
    echo "GitHub Release:   https://github.com/${GITHUB_REPO}/releases/tag/v${VERSION}"
    echo ""
    echo "Container images published to GHCR:"
    echo "  🔗 ${IMAGE_NAME}:${VERSION}"
    echo "  🔗 ${IMAGE_NAME}:latest"
    echo ""
    echo "Users can pull with:"
    printf "  ${BLUE}docker pull ${IMAGE_NAME}:${VERSION}${NC}\n"
    printf "  ${BLUE}docker pull ${IMAGE_NAME}:latest${NC}\n"
    echo ""
}

# Main release flow
main() {
    local bump_type=$1

    # Validate input
    if [ -z "$bump_type" ]; then
        echo "Usage: $0 {patch|minor|major}"
        echo ""
        echo "  patch - Bug fixes (0.1.0 -> 0.1.1)"
        echo "  minor - New features (0.1.0 -> 0.2.0)"
        echo "  major - Breaking changes (0.1.0 -> 1.0.0)"
        exit 1
    fi

    if [[ ! "$bump_type" =~ ^(patch|minor|major)$ ]]; then
        print_error "Invalid bump type: $bump_type"
        echo "Must be one of: patch, minor, major"
        exit 1
    fi

    print_header "🚀 Starting Release Process"
    print_info "Bump type: $bump_type"

    # Run all steps
    check_prerequisites
    validate_git_status
    run_tests
    bump_version "$bump_type"
    generate_changelog
    build_images
    push_images
    commit_and_tag
    push_to_github
    create_github_release
    display_summary
}

# Run main with arguments
main "$@"
