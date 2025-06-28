# pipeline/simplifier.py

import os
import json
from time import sleep
from pathlib import Path
from dotenv import load_dotenv

# 🌍 Load .env from root directory
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# 🔑 Get the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
use_gemini = False

try:
    if GEMINI_API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        use_gemini = True
        print(f"✅ SignSafe at your Service !")
    else:
        print("⚠️ SignSafe_API not found in .env. Using fallback.")
except Exception as e:
    print(f"❌ Error importing SignSafe or configuring it: {e}")
    use_gemini = False

# 📦 Load cache if it exists
CACHE_FILE = "pipeline/simplified_cache.json"
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        simplification_cache = json.load(f)
else:
    simplification_cache = {}

def simplify_clause(clause: str) -> str:
    """
    Simplify a single clause using Gemini or fallback. Caches results.
    """
    if clause in simplification_cache:
        return simplification_cache[clause]

    if not use_gemini:
        simplified = f"Simplified version of: {clause[:60]}..."
        simplification_cache[clause] = simplified
        return simplified

    try:
        prompt = f"Simplify this legal clause in plain English:\n\n{clause}"
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        simplified = response.text.strip()

        # Save to cache
        simplification_cache[clause] = simplified
        save_cache()
        return simplified

    except Exception as e:
        print(f"❌ SignSafe error: {e}")
        simplified = f"Simplified version of: {clause[:60]}..."
        simplification_cache[clause] = simplified
        return simplified

def batch_simplify_clauses(clauses: list, batch_size: int = 5) -> list:
    """
    Simplify multiple clauses in batches with cache & fallback support.
    """
    simplified_list = []
    for i in range(0, len(clauses), batch_size):
        batch = clauses[i:i + batch_size]
        for clause in batch:
            simplified = simplify_clause(clause)
            simplified_list.append({
                "original": clause,
                "simplified": simplified
            })
        sleep(1)  # Avoid quota throttling
    return simplified_list

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(simplification_cache, f, indent=2)
