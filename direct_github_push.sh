#!/bin/bash

# Direct GitHub push using API
echo "🚀 Direct GitHub Push Script"
echo "============================"
echo ""
echo "This script will push your Vehicle Maintenance App directly to GitHub"
echo "You'll need:"
echo "1. Your GitHub username"
echo "2. A Personal Access Token (create at https://github.com/settings/tokens)"
echo ""

read -p "Enter GitHub username: " USERNAME
read -s -p "Enter GitHub Personal Access Token: " TOKEN
echo ""

REPO_NAME="vehicle-maintenance-app"
API_BASE="https://api.github.com"

echo ""
echo "📦 Creating repository..."

# Create repository
CREATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$API_BASE/user/repos" \
  -d '{
    "name": "'$REPO_NAME'",
    "description": "Advanced vehicle maintenance tracking with Google Gemini AI integration",
    "private": false,
    "auto_init": false
  }')

HTTP_CODE=$(echo "$CREATE_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$CREATE_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "201" ]; then
  echo "✅ Repository created successfully!"
elif [ "$HTTP_CODE" = "422" ]; then
  echo "ℹ️  Repository already exists, updating..."
else
  echo "❌ Failed to create repository (HTTP $HTTP_CODE)"
  echo "$RESPONSE_BODY"
  exit 1
fi

echo ""
echo "📤 Uploading files..."

# Function to upload a file
upload_file() {
  local file_path=$1
  local file_content=$(base64 -w 0 "$file_path" 2>/dev/null || base64 "$file_path")

  local upload_response=$(curl -s -w "\n%{http_code}" -X PUT \
    -H "Authorization: token $TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "$API_BASE/repos/$USERNAME/$REPO_NAME/contents/$file_path" \
    -d '{
      "message": "Add '$file_path'",
      "content": "'$file_content'"
    }')

  local upload_code=$(echo "$upload_response" | tail -n1)

  if [ "$upload_code" = "201" ]; then
    echo "   ✓ $file_path"
  else
    echo "   ✗ $file_path (HTTP $upload_code)"
  fi
}

# Upload key files
for file in flask_app.py requirements.txt README.md DATABASE_STATUS.md .gitignore LICENSE initialize_db.py; do
  if [ -f "$file" ]; then
    upload_file "$file"
  fi
done

# Upload templates
for template in templates/*.html; do
  if [ -f "$template" ]; then
    upload_file "$template"
  fi
done

# Upload tests
for test_file in tests/e2e/*.py tests/*.py tests/*.ini; do
  if [ -f "$test_file" ]; then
    upload_file "$test_file"
  fi
done

echo ""
echo "✅ Upload complete!"
echo ""
echo "🎉 Your repository is available at:"
echo "   https://github.com/$USERNAME/$REPO_NAME"
echo ""
echo "Clone with:"
echo "   git clone https://github.com/$USERNAME/$REPO_NAME.git"