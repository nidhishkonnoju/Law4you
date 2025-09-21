import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# --- CONFIGURATION ---
# Load environment variables from your .env file
load_dotenv()
try:
    # Configure the Gemini API with your key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except (TypeError, ValueError) as e:
    print(f"ERROR: Could not configure Gemini API. Check GOOGLE_API_KEY. Details: {{e}}")
    exit()

# --- MODEL INITIALIZATION ---
# Initialize the models that will be used for different tasks.
text_model = genai.GenerativeModel('gemini-1.5-pro-latest')
vision_model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using Flash for faster image response

# --- CORE AI ANALYSIS FUNCTIONS ---

# Master prompt for all text-based analysis
MASTER_PROMPT = """
**Role:** You are an expert AI legal assistant for Indian citizens. Your task is to analyze a legal clause and provide a structured, easy-to-understand breakdown.

**Here is a perfect example of your task:**
* **Input Clause:** "The provisions of this Act shall have effect notwithstanding anything inconsistent therewith contained in any other law for the time being in force."
* **Your Output JSON:**
    ```json
    {{
        "simplified_text": "If any other law conflicts with this Act, this Act will be the one that applies.",
        "jargon_definitions": [
            {{"term": "Notwithstanding", "definition": "Means 'in spite of' or 'even if'."}},
            {{"term": "In force", "definition": "Currently valid and legally binding."}}
        ],
        "risk_score": 5,
        "questions_for_lawyer": [
            "Are there any specific existing laws that are known to conflict with this Act?",
            "Under what circumstances could this clause be challenged?"
        ]
    }}
    ```
---
**Now, perform the same analysis on the following user-provided clause.**

**User Clause:**
"{legal_text}"

**Your Instructions:**
Analyze the clause and return ONLY a single, valid JSON object with the exact keys shown in the example. Do not include any text, comments, or markdown formatting like ```json before or after the JSON object.
"""

def analyze_clause(legal_text: str) -> dict:
    """Analyzes a string of legal text using the Gemini Pro model."""
    if not legal_text or not legal_text.strip():
        return {"error": "Input text cannot be empty."}
    
    prompt = MASTER_PROMPT.format(legal_text=legal_text)
    
    try:
        response = text_model.generate_content(prompt)
        # Clean the response to ensure it's a valid JSON string
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "")
        analysis_dict = json.loads(cleaned_response_text)
        return analysis_dict
    except Exception as e:
        print(f"An error occurred during API call or JSON parsing: {{e}}")
        return {"error": "Failed to analyze the clause. The AI response may not be valid JSON."}

def analyze_image_clause(image_file) -> dict:
    """Analyzes a legal clause from an image file using the Gemini Flash model."""
    if not image_file:
        return {"error": "Image file cannot be empty."}

    try:
        # Open the image file
        img = Image.open(image_file)
        
        # Create a prompt that instructs the model to transcribe and then analyze
        vision_prompt = [
            "You are an expert in Indian law. First, accurately transcribe the text from this image of a legal document. Then, using only the transcribed text, perform a detailed legal analysis. Your final output must be ONLY a single, valid JSON object with the following keys: 'simplified_text', 'jargon_definitions', 'risk_score', and 'questions_for_lawyer'. Do not include the transcription or any other text in your final response.",
            img,
        ]
        
        response = vision_model.generate_content(vision_prompt)
        # Clean the response to ensure it's a valid JSON string
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "")
        analysis_dict = json.loads(cleaned_response_text)
        return analysis_dict
        
    except Exception as e:
        print(f"An error occurred during image analysis: {{e}}")
        return {"error": "Failed to analyze the image. It may be corrupt or in an unsupported format."}
