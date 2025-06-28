# pipeline/risk_analyzer.py

import os
import json
from pathlib import Path
from time import sleep
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# Load API key
OMNIDIM_API_KEY = os.getenv("OMNIDIM_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Flags
use_omnidim = bool(OMNIDIM_API_KEY)
use_gemini = bool(GEMINI_API_KEY)

# Try to import SignSafe
if use_gemini:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("✅ SignSafe ready for fallback risk analysis.")
    except Exception as e:
        print(f"⚠️ SignSafe setup failed: {e}")
        use_gemini = False

# Dummy risk cache
CACHE_FILE = "pipeline/risk_cache.json"
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        risk_cache = json.load(f)
else:
    risk_cache = {}

def analyze_risk(clause: str) -> dict:
    if clause in risk_cache:
        return risk_cache[clause]

    # Preferred: Omnidimension logic (placeholder)
    if use_omnidim:
        risk_level = "Medium"
        reason = "Omnidimension placeholder: Would flag this if clause contains ambiguity or harsh penalty."
        result = {"risk_level": risk_level, "reason": reason}
        risk_cache[clause] = result
        save_cache()
        return result

    # Fallback: Gemini
    elif use_gemini:
        prompt = (
            f"Analyze this legal clause for risk. Return a risk level (Low/Medium/High) "
            f"and a short explanation:\n\n{clause}"
        )
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()

            # Try parsing the response
            level = "Medium"
            if "high" in text.lower(): level = "High"
            elif "low" in text.lower(): level = "Low"

            result = {
                "risk_level": level,
                "reason": text
            }
            risk_cache[clause] = result
            save_cache()
            return result
        except Exception as e:
            print(f"❌ SafeSign risk analysis error: {e}")

    # Total fallback
    result = {
        "risk_level": "Unknown",
        "reason": "Risk analysis unavailable (no model active)"
    }
    risk_cache[clause] = result
    return result

def batch_analyze_risks(clauses: list, delay: int = 1) -> list:
    results = []
    for clause in clauses:
        result = analyze_risk(clause)
        results.append({
            "original": clause,
            "risk_level": result["risk_level"],
            "reason": result["reason"]
        })
        sleep(delay)
    return results

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(risk_cache, f, indent=2)
