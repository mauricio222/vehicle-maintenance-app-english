#!/usr/bin/env python3
"""
Direct push to GitHub using API - No git required!
"""

import os
import base64
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests")
    import requests

def push_to_github():
    print("🚀 GitHub Direct Push - Vehicle Maintenance App")
    print("=" * 60)
    print("")

    # Hardcoded credentials for automated push
    # NOTE: In production, use environment variables or secure input
    print("📝 Enter GitHub credentials:")
    print("(Create token at: https://github.com/settings/tokens)")
    print("")

    username = input("GitHub username: ").strip()
    token = input("GitHub Personal Access Token: ").strip()

    if not username or not token:
        print("❌ Credentials required!")
        return False

    repo_name = "vehicle-maintenance-app"
    api_base = "https://api.github.com"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Step 1: Create repository
    print("\n📦 Creating repository...")
    repo_data = {
        "name": repo_name,
        "description": "Advanced vehicle maintenance tracking with Google Gemini AI integration",
        "homepage": "https://github.com/mauricio222/vehicle-maintenance-app",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }

    response = requests.post(f"{api_base}/user/repos", headers=headers, json=repo_data)

    if response.status_code == 201:
        print("✅ Repository created!")
    elif response.status_code == 422:
        print("ℹ️  Repository exists, updating...")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        return False

    # Step 2: Upload files
    print("\n📤 Uploading files...")

    # Key files to upload
    files_to_upload = [
        "flask_app.py",
        "requirements.txt",
        "README.md",
        "DATABASE_STATUS.md",
        ".gitignore",
        "LICENSE",
        "initialize_db.py",
        ".env.example",
        "clean_db_final.py",
        "clean_mechanics.py",
        "verify_admin_user.py",
        "check_db_schema.py",
        "pytest.ini"
    ]

    # Add template files
    template_dir = Path("templates")
    if template_dir.exists():
        for template in template_dir.glob("*.html"):
            files_to_upload.append(str(template))

    # Add test files
    test_dir = Path("tests")
    if test_dir.exists():
        for test_file in test_dir.rglob("*.py"):
            files_to_upload.append(str(test_file))
        for conf_file in test_dir.glob("*.ini"):
            files_to_upload.append(str(conf_file))

    uploaded = 0
    failed = 0

    for filepath in files_to_upload:
        if not Path(filepath).exists():
            continue

        try:
            with open(filepath, 'rb') as f:
                content = f.read()

            # Encode content
            encoded = base64.b64encode(content).decode('ascii')

            # Upload file
            file_data = {
                "message": f"Add {filepath}",
                "content": encoded,
                "committer": {
                    "name": "Vehicle Maintenance App",
                    "email": "noreply@vehiclemaintenance.app"
                }
            }

            url = f"{api_base}/repos/{username}/{repo_name}/contents/{filepath}"
            response = requests.put(url, headers=headers, json=file_data)

            if response.status_code in [201, 200]:
                print(f"   ✓ {filepath}")
                uploaded += 1
            else:
                print(f"   ✗ {filepath} ({response.status_code})")
                failed += 1

        except Exception as e:
            print(f"   ✗ {filepath} (Error: {e})")
            failed += 1

    print(f"\n📊 Results: {uploaded} uploaded, {failed} failed")

    if uploaded > 0:
        print("\n✅ Push successful!")
        print(f"\n🎉 Repository available at:")
        print(f"   https://github.com/{username}/{repo_name}")
        print(f"\nClone with:")
        print(f"   git clone https://github.com/{username}/{repo_name}.git")
        return True
    else:
        print("\n❌ Push failed!")
        return False

if __name__ == "__main__":
    success = push_to_github()
    if not success:
        print("\n💡 Alternative: Upload manually at https://github.com/new")
        sys.exit(1)