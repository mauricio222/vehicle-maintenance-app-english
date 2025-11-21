import google.generativeai as genai

# Configure with API key
genai.configure(api_key='AIzaSyCChtV_fm5I4xK05hR8Gpp8INMqtS14PFI')

print("Testing Gemini API models...")
print("-" * 50)

# Try different model names
models_to_try = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro',
    'gemini-1.5-pro-latest',
    'gemini-pro',
    'gemini-1.0-pro',
    'gemini-1.0-pro-latest'
]

for model_name in models_to_try:
    try:
        print(f"\nTrying: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say hello in 3 words")
        print(f"✅ SUCCESS with {model_name}")
        print(f"   Response: {response.text[:100]}")
        break
    except Exception as e:
        print(f"❌ Failed: {str(e)[:100]}")