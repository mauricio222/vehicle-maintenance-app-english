import google.generativeai as genai

# Configure with API key
genai.configure(api_key='AIzaSyCChtV_fm5I4xK05hR8Gpp8INMqtS14PFI')

print("Listing all available models...")
print("-" * 50)

try:
    for model in genai.list_models():
        print(f"\nModel: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Supported methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")
    print("\nTrying direct model access...")
    # Try with the recommended free model from Dec 2024
    model_name = 'gemini-2.0-flash-exp'
    try:
        print(f"\nTrying: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say hello")
        print(f"✅ SUCCESS with {model_name}")
        print(f"Response: {response.text}")
    except Exception as e2:
        print(f"Failed: {e2}")