# Release Guide

This document describes the release process for docling-forge.

## Overview

The project uses:
- **Semantic Versioning** (`MAJOR.MINOR.PATCH`)
- **Conventional Commits** for changelog generation
- **Local release workflow** (no GitHub Actions)
- **Multi-platform builds** (linux/amd64, linux/arm64)
- **GitHub Container Registry** (GHCR) for image hosting

## Prerequisites

### Required Tools

1. **Python tools:**
   ```bash
   pip install bump2version
   ```

2. **Changelog generation:**
   ```bash
   # macOS
   brew install git-cliff

   # Linux/Other
   cargo install git-cliff
   ```

3. **GitHub CLI:**
   ```bash
   # macOS
   brew install gh

   # Linux
   sudo apt install gh

   # Authenticate
   gh auth login
   ```

4. **Docker with Buildx:**
   ```bash
   # Verify Buildx is available
   docker buildx version
   ```

### GHCR Authentication

Create a GitHub Personal Access Token (PAT) with `write:packages` scope:

1. Go to https://github.com/settings/tokens/new?scopes=write:packages
2. Generate token
3. Login to GHCR:
   ```bash
   export GITHUB_TOKEN=your_token_here
   echo $GITHUB_TOKEN | docker login ghcr.io -u rennochj --password-stdin
   ```

## Conventional Commits

Use conventional commit messages for automatic changelog generation:

- `feat:` - New features (triggers minor version bump)
- `fix:` - Bug fixes (triggers patch version bump)
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks
- `refactor:` - Code refactoring
- `test:` - Test updates
- `perf:` - Performance improvements

**Examples:**
```bash
git commit -m "feat: add support for EPUB format"
git commit -m "fix: resolve memory leak in batch processing"
git commit -m "docs: update installation instructions"
```

## Release Process

### Quick Release (Recommended)

Use the automated release script:

```bash
# Patch release (0.1.0 → 0.1.1) - for bug fixes
make release-patch

# Minor release (0.1.0 → 0.2.0) - for new features
make release-minor

# Major release (0.1.0 → 1.0.0) - for breaking changes
make release-major
```

### What the Release Script Does

The `scripts/release.sh` script automates the entire release process:

1. ✅ **Pre-flight checks:**
   - Validates all required tools are installed
   - Checks git status (no uncommitted changes)
   - Verifies you're on master/main branch
   - Confirms GitHub CLI is authenticated
   - Checks GHCR authentication

2. ✅ **Testing:**
   - Runs test suite (`uv run pytest`)
   - Fails if any tests fail

3. ✅ **Version bump:**
   - Updates `VERSION` file
   - Updates `pyproject.toml`
   - Updates `.bumpversion.cfg`

4. ✅ **Changelog:**
   - Generates/updates `CHANGELOG.md` from conventional commits
   - Uses `git-cliff` for formatting

5. ✅ **Multi-platform build:**
   - Sets up Docker Buildx
   - Builds for linux/amd64 and linux/arm64
   - Creates multiple tags:
     - `ghcr.io/rennochj/docling-forge:0.1.0` (specific)
     - `ghcr.io/rennochj/docling-forge:0.1` (minor)
     - `ghcr.io/rennochj/docling-forge:0` (major)
     - `ghcr.io/rennochj/docling-forge:latest`

6. ✅ **Push to GHCR:**
   - Authenticates with GitHub Container Registry
   - Pushes all platform variants
   - Pushes all tags

7. ✅ **Git operations:**
   - Commits version changes
   - Creates git tag (e.g., `v0.1.0`)
   - Pushes code and tags to GitHub

8. ✅ **GitHub release:**
   - Creates GitHub release with changelog
   - Links to the git tag

9. ✅ **Summary:**
   - Displays release information
   - Shows pull commands for users

### Manual Step-by-Step Release

If you need more control, use individual commands:

```bash
# 1. Check current version
make show-version

# 2. Run tests
make test-local

# 3. Bump version (choose one)
bump2version patch   # 0.1.0 → 0.1.1
bump2version minor   # 0.1.0 → 0.2.0
bump2version major   # 0.1.0 → 1.0.0

# 4. Generate changelog
make changelog

# 5. Setup buildx (first time only)
make setup-buildx

# 6. Build multi-platform images
make build-multiplatform

# 7. Push to GHCR
make push-ghcr

# 8. Commit and tag
git add VERSION pyproject.toml .bumpversion.cfg CHANGELOG.md
git commit -m "chore(release): prepare for v$(cat VERSION)"
git tag -a "v$(cat VERSION)" -m "Release v$(cat VERSION)"

# 9. Push to GitHub
git push && git push --tags

# 10. Create GitHub release
gh release create "v$(cat VERSION)" \
  --title "v$(cat VERSION)" \
  --notes-file <(git-cliff --unreleased --strip header)
```

## Versioning Guidelines

### Patch Release (0.1.0 → 0.1.1)

Use for:
- Bug fixes
- Security patches
- Documentation updates
- Performance improvements (non-breaking)

**Example commits:**
```
fix: correct PDF extraction error
docs: update troubleshooting guide
perf: optimize image processing
```

### Minor Release (0.1.0 → 0.2.0)

Use for:
- New features
- New file format support
- New CLI options
- Enhancements (backward compatible)

**Example commits:**
```
feat: add EPUB format support
feat: add --parallel-processing option
feat: implement progress bar for batch conversion
```

### Major Release (0.1.0 → 1.0.0)

Use for:
- Breaking changes
- API changes
- CLI argument changes
- Removed features
- Major refactoring

**Example commits:**
```
feat!: change default output format to JSON
feat!: remove deprecated --legacy-mode flag
refactor!: restructure CLI command hierarchy
```

## Post-Release

After a successful release:

1. **Verify the release:**
   ```bash
   # Check GitHub release page
   open https://github.com/rennochj/docling-forge/releases

   # Test pulling the image
   docker pull ghcr.io/rennochj/docling-forge:latest
   docker pull ghcr.io/rennochj/docling-forge:0.1.0
   ```

2. **Test the image:**
   ```bash
   docker run --rm ghcr.io/rennochj/docling-forge:latest --version
   ```

3. **Announce the release:**
   - Update project documentation
   - Post in relevant channels
   - Update dependent projects

## Troubleshooting

### "Not logged in to GHCR"

**Solution:**
```bash
# Create/use GitHub Personal Access Token
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
echo $GITHUB_TOKEN | docker login ghcr.io -u rennochj --password-stdin
```

### "GitHub CLI not authenticated"

**Solution:**
```bash
gh auth login
# Follow the prompts to authenticate
```

### "Uncommitted changes"

**Solution:**
```bash
# Commit or stash your changes first
git status
git add .
git commit -m "fix: your changes"
# Then retry release
```

### "Tests failed"

**Solution:**
```bash
# Fix failing tests first
uv run pytest tests/ -v
# Then retry release
```

### "Builder not found"

**Solution:**
```bash
# Setup buildx
make setup-buildx
# Then retry release
```

### "Permission denied pushing to GHCR"

**Solution:**
1. Verify your GitHub token has `write:packages` scope
2. Re-authenticate:
   ```bash
   docker logout ghcr.io
   echo $GITHUB_TOKEN | docker login ghcr.io -u rennochj --password-stdin
   ```

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Support

For release-related issues:
- Check this guide first
- Review [CHANGELOG.md](CHANGELOG.md)
- Check [GitHub Issues](https://github.com/rennochj/docling-forge/issues)
- Ask in GitHub Discussions
