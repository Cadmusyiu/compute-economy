#!/usr/bin/env python3
"""
compute-economy: Git-based research repo setup

Initializes the compute-economy folder as a git repo with proper structure.
Pushes to GitHub so Cadmus can track changes.
"""

import os
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent

GITIGNORE_CONTENT = """
# Python
__pycache__/
*.pyc
.env
venv/

# Data with personal tokens
raw_data/*.json

# OS files
.DS_Store
Thumbs.db

# Keep CSV (timeseries data)
!gpu_price_timeseries.csv
"""

README_CONTENT = """
# Compute Economy Research

> Auto-assessment repo for GPU compute market monitoring.
> See ASSESSMENT.md for latest market health report.

## Quick Start

```bash
python3 scripts/collect_daily.py    # Collect today's data
python3 scripts/assess_market.py     # Generate assessment
python3 scripts/alert_check.py       # Check alerts
```

## Structure
- `scripts/` — automation scripts
- `raw_data/` — daily data dumps (gitignored)
- `dashboard/` — visualization
- `notebooks/` — Jupyter analysis
- `ASSESSMENT.md` — latest auto-generated report
- `RESEARCH_LOG.md` — daily research log
"""


def init_git():
    """Initialize git repo if not already"""
    if (REPO_DIR / ".git").exists():
        print("✅ Git repo already initialized")
        return
    
    subprocess.run(["git", "init"], cwd=REPO_DIR, check=True)
    print("✅ Git repo initialized")


def create_gitignore():
    gitignore = REPO_DIR / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(GITIGNORE_CONTENT.strip())
        print("✅ .gitignore created")


def make_first_commit():
    """Stage and commit initial files"""
    subprocess.run(["git", "add", "."], cwd=REPO_DIR, check=True)
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    
    if result.stdout.strip():
        subprocess.run(
            ["git", "commit", "-m", "feat: init compute economy research repo\n\nAuto-assessment pipeline for GPU compute market monitoring."],
            cwd=REPO_DIR, check=True
        )
        print("✅ Initial commit made")
    else:
        print("ℹ️  Nothing to commit")


def main():
    print("=" * 50)
    print("Compute Economy — Repo Setup")
    print("=" * 50)
    
    # Create .gitkeep in empty dirs
    for d in ["raw_data", "dashboard/plots", "notebooks"]:
        keep = REPO_DIR / d / ".gitkeep"
        keep.parent.mkdir(parents=True, exist_ok=True)
        keep.touch()
    
    init_git()
    create_gitignore()
    make_first_commit()
    
    print("\n✅ Repo setup complete!")
    print(f"📂 {REPO_DIR}")
    
    # Suggest GitHub remote
    print("\n💡 To push to GitHub:")
    print("   gh repo create cadmus/compute-economy --private --source=. --remote=origin --push")
    print("   # or:")
    print("   git remote add origin git@github.com:CadmusYiu/compute-economy.git")
    print("   git push -u origin main")


if __name__ == "__main__":
    main()
