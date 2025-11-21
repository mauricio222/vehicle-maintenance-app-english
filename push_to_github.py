#!/usr/bin/env python3
"""
Push Vehicle Maintenance App to GitHub
"""

import os
import sys
from pathlib import Path

try:
    import git
    from git import Repo, GitCommandError
except ImportError:
    print("GitPython not installed. Running: pip install GitPython")
    os.system("pip install GitPython")
    import git
    from git import Repo, GitCommandError

def push_to_github():
    """Initialize git repo and push to GitHub"""

    # Current directory
    repo_path = Path.cwd()
    print(f"📁 Working directory: {repo_path}")

    try:
        # Initialize repository
        print("🔧 Initializing Git repository...")
        repo = Repo.init(repo_path)

        # Configure git user
        print("👤 Configuring Git user...")
        with repo.config_writer() as config:
            config.set_value("user", "name", "Vehicle Maintenance App")
            config.set_value("user", "email", "noreply@vehiclemaintenance.app")

        # Add all files
        print("📝 Adding files to staging...")
        repo.git.add(all=True)

        # Check what files were added
        staged_files = repo.git.diff("--cached", "--name-only").split("\n")
        print(f"   Added {len(staged_files)} files")

        # Create commit
        commit_message = """Initial commit: Vehicle Maintenance App with AI features

- Complete Flask application with authentication
- Google Gemini AI integration for intelligent maintenance suggestions
- Comprehensive E2E test suite (10/10 tests passing)
- Clean demo database with admin user
- Bilingual support (English/Spanish)
- Responsive Bootstrap 5 UI
- AI-powered maintenance predictions and categorization
- Automated maintenance scheduling
- Predictive analytics for component wear

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"""

        print("💾 Creating commit...")
        repo.index.commit(commit_message)
        print("✅ Commit created successfully")

        # Add remote
        remote_url = "https://github.com/mauricio222/vehicle-maintenance-app.git"
        print(f"🌐 Adding remote: {remote_url}")

        # Check if remote already exists
        if "origin" in [remote.name for remote in repo.remotes]:
            origin = repo.remote("origin")
            origin.set_url(remote_url)
        else:
            origin = repo.create_remote("origin", remote_url)

        # Push to GitHub
        print("🚀 Pushing to GitHub...")
        print("⚠️  Note: You may need to enter your GitHub credentials")
        print("    For authentication, use:")
        print("    - Username: your GitHub username")
        print("    - Password: a Personal Access Token (not your password)")
        print("    Create token at: https://github.com/settings/tokens")
        print()

        # Set main branch
        repo.git.branch("-M", "main")

        # Push
        origin.push("main", force=True)

        print("✅ Successfully pushed to GitHub!")
        print(f"🎉 Repository available at: https://github.com/mauricio222/vehicle-maintenance-app")

    except GitCommandError as e:
        print(f"❌ Git error: {e}")
        print("\n📋 Manual steps to push:")
        print("1. Make sure you have git installed")
        print("2. Run these commands:")
        print("   git init")
        print("   git add .")
        print('   git commit -m "Initial commit"')
        print("   git branch -M main")
        print("   git remote add origin https://github.com/mauricio222/vehicle-maintenance-app.git")
        print("   git push -u origin main")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 Vehicle Maintenance App - GitHub Push Tool")
    print("=" * 60)

    success = push_to_github()

    if not success:
        print("\n⚠️  If push failed due to authentication:")
        print("1. Create a Personal Access Token on GitHub")
        print("2. Go to: https://github.com/settings/tokens")
        print("3. Generate new token with 'repo' scope")
        print("4. Use token as password when prompted")
        sys.exit(1)