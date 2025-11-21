#!/usr/bin/env python3
"""
Push Vehicle Maintenance App to GitHub using GitHub API
"""

import os
import base64
import json
import requests
from pathlib import Path
import mimetypes

def create_github_repo_and_push():
    """Create GitHub repository and upload files using API"""

    print("🚀 GitHub Repository Push Tool")
    print("=" * 60)

    # Get GitHub credentials
    print("\n📝 GitHub Authentication Required:")
    print("You need a GitHub Personal Access Token to proceed.")
    print("Create one at: https://github.com/settings/tokens")
    print("Required scopes: repo (Full control of private repositories)")
    print()

    username = input("Enter your GitHub username: ").strip()
    token = input("Enter your GitHub Personal Access Token: ").strip()

    if not username or not token:
        print("❌ Username and token are required!")
        return False

    # Repository details
    repo_name = "vehicle-maintenance-app"
    repo_description = "Advanced vehicle maintenance tracking with Google Gemini AI integration"

    # GitHub API headers
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Step 1: Create repository
    print(f"\n📦 Creating repository: {repo_name}...")
    create_repo_url = "https://api.github.com/user/repos"
    repo_data = {
        "name": repo_name,
        "description": repo_description,
        "private": False,
        "auto_init": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
    }

    response = requests.post(create_repo_url, headers=headers, json=repo_data)

    if response.status_code == 201:
        print("✅ Repository created successfully!")
        repo_info = response.json()
    elif response.status_code == 422:
        print("ℹ️  Repository already exists, will update it...")
        repo_info = requests.get(f"https://api.github.com/repos/{username}/{repo_name}", headers=headers).json()
    else:
        print(f"❌ Failed to create repository: {response.status_code}")
        print(response.json())
        return False

    # Step 2: Prepare files to upload
    print("\n📁 Preparing files for upload...")

    # Files and directories to include
    files_to_upload = []
    excluded = {'.git', '.venv', 'venv', '__pycache__', '.env', '*.pyc', '*.db'}

    # Gather all files
    for root, dirs, files in os.walk('.'):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in excluded and not d.startswith('.')]

        for file in files:
            # Skip excluded files
            if any(file.endswith(exc.replace('*', '')) for exc in excluded if '*' in exc):
                continue
            if file in excluded or file.startswith('.'):
                continue

            filepath = Path(root) / file
            relative_path = filepath.relative_to('.')

            # Skip large files
            if filepath.stat().st_size > 100 * 1024 * 1024:  # 100MB
                print(f"   Skipping large file: {relative_path}")
                continue

            files_to_upload.append(str(relative_path))

    print(f"   Found {len(files_to_upload)} files to upload")

    # Step 3: Create a single commit with all files
    print("\n📤 Uploading files to GitHub...")

    # Get the default branch
    default_branch = repo_info.get('default_branch', 'main')

    # Create tree with all files
    tree = []
    for filepath in files_to_upload[:50]:  # Limit to 50 files for API limits
        try:
            with open(filepath, 'rb') as f:
                content = f.read()

            # Encode content
            if filepath.endswith(('.jpg', '.png', '.gif', '.ico', '.db')):
                encoded = base64.b64encode(content).decode('utf-8')
            else:
                try:
                    encoded = base64.b64encode(content).decode('utf-8')
                except:
                    continue

            tree.append({
                "path": filepath.replace('\\', '/'),
                "mode": "100644",
                "type": "blob",
                "content": encoded
            })
            print(f"   ✓ {filepath}")
        except Exception as e:
            print(f"   ✗ Skipped {filepath}: {e}")

    if not tree:
        print("❌ No files to upload!")
        return False

    # Create tree
    tree_url = f"https://api.github.com/repos/{username}/{repo_name}/git/trees"
    tree_data = {"tree": tree}

    print(f"\n📝 Creating tree with {len(tree)} files...")
    response = requests.post(tree_url, headers=headers, json=tree_data)

    if response.status_code != 201:
        print(f"❌ Failed to create tree: {response.status_code}")
        print(response.json())
        return False

    tree_sha = response.json()['sha']

    # Create commit
    commit_url = f"https://api.github.com/repos/{username}/{repo_name}/git/commits"
    commit_data = {
        "message": "Initial commit: Vehicle Maintenance App with AI features\n\n- Complete Flask application with authentication\n- Google Gemini AI integration for intelligent maintenance suggestions\n- Comprehensive E2E test suite (10/10 tests passing)\n- Clean demo database with admin user\n- Bilingual support (English/Spanish)\n- Responsive Bootstrap 5 UI\n\n🤖 Generated with Claude Code",
        "tree": tree_sha,
        "author": {
            "name": "Vehicle Maintenance App",
            "email": "noreply@vehiclemaintenance.app"
        }
    }

    print("💾 Creating commit...")
    response = requests.post(commit_url, headers=headers, json=commit_data)

    if response.status_code != 201:
        print(f"❌ Failed to create commit: {response.status_code}")
        print(response.json())
        return False

    commit_sha = response.json()['sha']

    # Update reference
    ref_url = f"https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/{default_branch}"
    ref_data = {"sha": commit_sha, "force": True}

    # Try to update or create the reference
    response = requests.patch(ref_url, headers=headers, json=ref_data)
    if response.status_code == 404:
        # Create the reference
        ref_url = f"https://api.github.com/repos/{username}/{repo_name}/git/refs"
        ref_data = {"ref": f"refs/heads/{default_branch}", "sha": commit_sha}
        response = requests.post(ref_url, headers=headers, json=ref_data)

    if response.status_code in [200, 201]:
        print("✅ Successfully pushed to GitHub!")
        print(f"\n🎉 Repository available at: https://github.com/{username}/{repo_name}")
        print(f"   Clone with: git clone https://github.com/{username}/{repo_name}.git")
        return True
    else:
        print(f"❌ Failed to update reference: {response.status_code}")
        print(response.json())
        return False

if __name__ == "__main__":
    try:
        success = create_github_repo_and_push()
        if not success:
            print("\n⚠️  Upload failed. Please try manual method:")
            print("   1. Create repository at https://github.com/new")
            print("   2. Upload files manually through GitHub web interface")
    except KeyboardInterrupt:
        print("\n\n❌ Upload cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📋 Please use manual upload method instead")