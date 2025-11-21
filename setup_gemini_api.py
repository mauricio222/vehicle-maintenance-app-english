#!/usr/bin/env python3
"""
Setup script for configuring Gemini API key for the Vehicle Maintenance App
"""
import os
import sys
from pathlib import Path

print("=" * 60)
print("GEMINI API SETUP FOR VEHICLE MAINTENANCE APP")
print("=" * 60)
print("\nThis app now uses Gemini 1.5 Flash (Free Tier)")
print("\n📋 How to get your FREE Gemini API key:")
print("-" * 60)
print("1. Go to: https://aistudio.google.com/app/apikey")
print("2. Sign in with your Google account")
print("3. Click 'Create API Key'")
print("4. Select 'Create API key in new project'")
print("5. Copy the generated API key")
print("-" * 60)

print("\n🆓 Free Tier Limits:")
print("  • 1,500 requests per day")
print("  • 1 million tokens per minute")
print("  • 1.5 million tokens per day")
print("  • No credit card required!")

print("\n✨ Model: gemini-1.5-flash")
print("  • Latest free tier model")
print("  • Fast response times")
print("  • Great for maintenance suggestions")

print("\n" + "=" * 60)

# Check if .env file exists
env_path = Path('.env')
if not env_path.exists():
    print("❌ Error: .env file not found!")
    print("Please run the app setup first.")
    sys.exit(1)

# Read current .env content
with open(env_path, 'r') as f:
    env_content = f.read()

# Check current API key status
if 'GEMINI_API_KEY=' in env_content:
    lines = env_content.split('\n')
    for line in lines:
        if line.startswith('GEMINI_API_KEY='):
            current_value = line.split('=', 1)[1].strip()
            if current_value and current_value != '':
                print(f"\n✅ API Key already configured (starts with: {current_value[:10]}...)")
                update = input("\nDo you want to update it? (y/n): ").lower()
                if update != 'y':
                    print("Keeping existing API key.")
                    sys.exit(0)
            break

# Get API key from user
print("\nPaste your Gemini API key below (or press Enter to skip):")
api_key = input("API Key: ").strip()

if not api_key:
    print("\n⚠️  No API key provided. AI features will be disabled.")
    print("You can add it later by running this script again.")
    sys.exit(0)

# Update .env file
lines = env_content.split('\n')
updated = False
new_lines = []

for line in lines:
    if line.startswith('GEMINI_API_KEY='):
        new_lines.append(f'GEMINI_API_KEY={api_key}')
        updated = True
    else:
        new_lines.append(line)

# Write updated content
with open(env_path, 'w') as f:
    f.write('\n'.join(new_lines))

print("\n✅ API key successfully configured!")
print("\n🚀 Next steps:")
print("1. Restart the Flask app for changes to take effect")
print("2. The AI suggestion features will now be enabled")
print("3. Test by creating a maintenance record and using the AI suggestion buttons")

print("\n" + "=" * 60)
print("Setup complete! Enjoy the AI-powered features!")
print("=" * 60)