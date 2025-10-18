---
description: Analyze current changes and commit with a robust, meaningful message
---

You are tasked with committing the current changes to git with a high-quality commit message.

# Instructions

1. **Analyze Changes**: Run `git status` and `git diff` to understand what has changed
2. **Determine Commit Type**: Based on the changes, determine the appropriate conventional commit type:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Test changes
   - `chore:` - Maintenance tasks
   - `perf:` - Performance improvements
   - `style:` - Code formatting

3. **Generate Message**: Create a commit message with:
   - **Subject line**: Brief summary (50-72 chars) following conventional commits format
   - **Body**: Detailed explanation of what changed and why (wrap at 72 chars)
   - **Footer**: Include the Claude Code signature

4. **Commit**: Execute the git commit with the generated message

# Commit Message Format

```
<type>(<scope>): <subject>

<body paragraph 1>

<body paragraph 2 if needed>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

# Requirements

- Subject line must be concise and descriptive
- Use present tense ("add feature" not "added feature")
- Body should explain WHAT changed and WHY (not HOW - the code shows that)
- If there are multiple unrelated changes, suggest splitting into multiple commits
- Stage all relevant files before committing

# After Committing

- Display the commit message
- Show the commit SHA
- Confirm success
