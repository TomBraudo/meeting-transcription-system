# Git Repository Setup - Step by Step

## Option 1: Using GitHub CLI (Recommended if installed)

### 1. Initialize Git Repository
```bash
git init
```

### 2. Add All Files
```bash
git add .
```

### 3. Make First Commit
```bash
git commit -m "Initial commit: Meeting transcription system backend"
```

### 4. Create GitHub Repository and Push (using GitHub CLI)
```bash
# Create repo on GitHub (make sure you're logged in: gh auth login)
gh repo create meeting-transcription-system --public --source=. --remote=origin --push
```

---

## Option 2: Manual Setup (Standard Method)

### 1. Initialize Git Repository
```bash
git init
```

### 2. Add All Files
```bash
git add .
```

### 3. Make First Commit
```bash
git commit -m "Initial commit: Meeting transcription system backend"
```

### 4. Create Repository on GitHub
- Go to https://github.com/new
- Repository name: `meeting-transcription-system` (or your preferred name)
- Choose Public or Private
- **DO NOT** initialize with README, .gitignore, or license (we already have files)
- Click "Create repository"

### 5. Add Remote and Push
```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/meeting-transcription-system.git

# Or if using SSH:
# git remote add origin git@github.com:YOUR_USERNAME/meeting-transcription-system.git

# Rename default branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Complete Command Sequence (Copy-Paste Ready)

**For HTTPS:**
```bash
git init
git add .
git commit -m "Initial commit: Meeting transcription system backend"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/meeting-transcription-system.git
git push -u origin main
```

**For SSH:**
```bash
git init
git add .
git commit -m "Initial commit: Meeting transcription system backend"
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/meeting-transcription-system.git
git push -u origin main
```

---

## Notes

- Replace `YOUR_USERNAME` with your actual GitHub username
- Replace `meeting-transcription-system` with your preferred repository name
- Make sure you have a `.env` file locally (it's gitignored) before committing
- The `.env.example` file will be committed (it's safe, no secrets)

---

## Verify Setup

After pushing, verify:
```bash
git remote -v  # Should show your remote URL
git status     # Should show "nothing to commit, working tree clean"
```

Then visit: `https://github.com/YOUR_USERNAME/meeting-transcription-system`

