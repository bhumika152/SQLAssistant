# scripts/test_gemini_working.py
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY or API_KEY == "your_gemini_api_key_here":
    print("❌ Please set your GOOGLE_API_KEY in .env file")
else:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        
        print("🧪 Testing available models for SQL generation...")
        
        # Test the models that should work
        test_models = [
            "gemini-2.0-flash",
            "gemini-2.0-flash-001", 
            "gemini-flash-latest",
            "gemini-pro-latest",
            "gemini-2.5-flash"
        ]
        
        test_prompt = "Show me all employees in the engineering department"
        
        for model_name in test_models:
            try:
                print(f"\n🔧 Testing {model_name}...")
                model = genai.GenerativeModel(model_name)
                
                prompt_text = f"""
                Convert this to PostgreSQL SQL: {test_prompt}
                
                Tables: 
                - departments(id, name)
                - employees(id, name, department_id, email, salary)
                
                Return only SQL, no explanations.
                """
                
                response = model.generate_content(prompt_text)
                sql = response.text.strip()
                
                print(f"✅ {model_name} SUCCESS!")
                print(f"   Response: {sql}")
                
            except Exception as e:
                print(f"❌ {model_name} failed: {e}")
                
    except Exception as e:
        print(f"❌ Gemini API error: {e}")