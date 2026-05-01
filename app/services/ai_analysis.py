import os
import json
import pdfplumber
import docx
import re
import asyncio
from typing import List, Optional, Any, Dict
from google import genai
from google.genai import types
from openai import OpenAI
from app.core.config import settings

class AIAnalysisService:
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        if self.gemini_key:
            self.client = genai.Client(api_key=self.gemini_key)
            self.model_name = 'gemini-1.5-flash'
        else:
            self.client = None
            
        self.nvidia_key = settings.NVIDIA_API_KEY
        self.nvidia_base_url = settings.NVIDIA_BASE_URL
        if self.nvidia_key:
            self.nvidia_client = OpenAI(
                base_url=self.nvidia_base_url,
                api_key=self.nvidia_key
            )
        else:
            self.nvidia_client = None

    async def extract_text_from_file(self, file_path: str) -> str:
        """Extracts raw text from PDF or DOCX files."""
        extension = os.path.splitext(file_path)[1].lower()
        text = ""
        
        try:
            if extension == ".pdf":
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            elif extension == ".docx":
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""
            
        return text.strip()

    async def analyze_document(self, file_path: str) -> dict:
        """
        Analyzes the document using a multimodal approach with Gemini 1.5.
        """
        if not self.client:
            raise ValueError("Gemini API Key is not configured.")

        # 1. EXTRACT TEXT LOCALLY (as fallback/context)
        raw_text = await self.extract_text_from_file(file_path)
        
        # 2. EMERGENCY REGEX FALLBACK
        regex_data = self._extract_contact_info_fallback(raw_text)
        
        # 3. ATTEMPT NVIDIA ANALYSIS FIRST (As requested by user)
        if self.nvidia_client:
            try:
                print(f"DEBUG: Attempting analysis with NVIDIA Mistral...")
                nvidia_data = await self._analyze_with_nvidia(raw_text)
                if nvidia_data:
                    nvidia_data["status"] = "success"
                    # Merge regex findings
                    if not nvidia_data.get("contact", {}).get("phone") and regex_data["phone"]:
                        nvidia_data.setdefault("contact", {})["phone"] = regex_data["phone"]
                    if not nvidia_data.get("contact", {}).get("email") and regex_data["email"]:
                        nvidia_data.setdefault("contact", {})["email"] = regex_data["email"]
                    
                    return self._sanitize_data(nvidia_data)
            except Exception as e:
                print(f"DEBUG: NVIDIA Analysis Error: {str(e)}")

        # 4. ATTEMPT AI ANALYSIS WITH EXPANDED FALLBACK (Gemini)
        # List of models to try in order of preference
        # We use various versions to ensure compatibility across different API tiers/regions
        models_to_try = [
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro",
            "gemini-2.0-flash-exp"
        ]
        
        prompt = self._get_analysis_prompt()
        last_error = None
        
        # Read file bytes for multimodal analysis if it's a PDF
        file_bytes = None
        mime_type = "application/pdf" if file_path.lower().endswith('.pdf') else None
        if mime_type:
            try:
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
            except:
                file_bytes = None

        for model in models_to_try:
            try:
                print(f"DEBUG: Attempting analysis with model: {model}")
                
                contents = []
                if file_bytes and mime_type:
                    # Multimodal content: PDF + Prompt
                    contents = [
                        types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                        types.Part.from_text(text=prompt)
                    ]
                else:
                    # Text-only content
                    contents = [f"{prompt}\n\nDOCUMENT CONTENT:\n{raw_text[:30000]}"]

                # We use a safety setting to avoid empty responses on harmless educational content
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.1,
                        top_p=0.95,
                        top_k=40
                    )
                )
                
                if not response.text:
                    print(f"DEBUG: Model {model} returned empty response.")
                    continue

                clean_text = response.text.strip()
                # Clean markdown blocks if present
                if clean_text.startswith("```json"): 
                    clean_text = clean_text[7:].split("```")[0].strip()
                elif clean_text.startswith("```"): 
                    clean_text = clean_text[3:].split("```")[0].strip()
                
                # Try to fix common JSON issues if parsing fails
                try:
                    data = json.loads(clean_text)
                except json.JSONDecodeError:
                    # Attempt a simple cleanup: remove trailing commas before closing braces/brackets
                    clean_text = re.sub(r',\s*([\]}])', r'\1', clean_text)
                    data = json.loads(clean_text)

                data["status"] = "success"
                
                # Merge regex findings if AI missed them
                if not data.get("contact", {}).get("phone") and regex_data["phone"]:
                    data.setdefault("contact", {})["phone"] = regex_data["phone"]
                if not data.get("contact", {}).get("email") and regex_data["email"]:
                    data.setdefault("contact", {})["email"] = regex_data["email"]
                    
                print(f"DEBUG: Successfully extracted data using {model}")
                
                # FINAL POLISH: Recursively remove "NOT FOUND", "N/A", "None" strings
                return self._sanitize_data(data)

            except Exception as e:
                print(f"DEBUG: Gemini Analysis Error ({model}): {str(e)}")
                await asyncio.sleep(1) # Small delay before retry
                continue

        # If all models failed
        print(f"CRITICAL ERROR: All Gemini models failed for {file_path}")
        fname = os.path.basename(file_path).split("_", 1)[-1] if "_" in file_path else os.path.basename(file_path)
        return self._get_fallback_data(fname, "AI Analysis failed after trying all models. Check API logs for details.", regex_data)

    async def _analyze_with_nvidia(self, text: str) -> Optional[dict]:
        """Analyzes text using Nvidia Mistral-7B-Instruct."""
        if not self.nvidia_client:
            return None

        prompt = self._get_analysis_prompt()
        
        try:
            # We use Mistral-7B-Instruct-v0.3 as requested
            completion = self.nvidia_client.chat.completions.create(
                model="mistralai/mistral-7b-instruct-v0.3",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured JSON data from educational documents."},
                    {"role": "user", "content": f"{prompt}\n\nDOCUMENT CONTENT:\n{text[:10000]}"}
                ],
                temperature=0.2,
                top_p=0.7,
                max_tokens=2048,
                stream=False # We want the full JSON at once for parsing
            )

            response_text = completion.choices[0].message.content.strip()
            
            # Clean markdown blocks if present
            if response_text.startswith("```json"): 
                response_text = response_text[7:].split("```")[0].strip()
            elif response_text.startswith("```"): 
                response_text = response_text[3:].split("```")[0].strip()
            
            return json.loads(response_text)
        except Exception as e:
            print(f"DEBUG: NVIDIA Mistral error: {e}")
            return None

    def _sanitize_data(self, data: Any) -> Any:
        """Recursively replaces 'Not Found', 'N/A', etc. with null."""
        if isinstance(data, dict):
            return {k: self._sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(v) for v in data]
        elif isinstance(data, str):
            lowered = data.lower().strip()
            if lowered in ["not found", "n/a", "none", "null", "not available", "unknown"]:
                return None
        return data

    def _extract_contact_info_fallback(self, text: str) -> dict:
        """Uses Regex to find email and phone if AI fails."""
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        # More robust phone regex for Indian/International numbers
        phones = re.findall(r'(\+?\d{1,4}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{4,6}', text)
        
        return {
            "email": emails[0] if emails else None,
            "phone": phones[0] if phones else None
        }

    def _get_fallback_data(self, name: str, error_msg: str, regex_data: dict = None) -> dict:
        """Returns a safe data structure when analysis fails."""
        return {
            "institute_name": name or "Analysis Failed",
            "institute_tagline": "AI Analysis failed: " + (error_msg[:100] if error_msg else "Unknown issue"),
            "status": "error",
            "contact": {
                "phone": regex_data.get("phone") if regex_data else None,
                "email": regex_data.get("email") if regex_data else None,
                "website": None,
                "address": None,
                "branches": []
            },
            "courses": [],
            "modules": [],
            "learning_outcomes": [],
            "tools_technologies": [],
            "industry_scope": [],
            "job_roles": [],
            "partners": [],
            "highlights": [],
            "faqs": [],
            "error_detail": error_msg
        }

    def _get_analysis_prompt(self) -> str:
        return """
You are an expert document analyst for the coaching and education industry. 
When a PDF or document is uploaded, extract ALL information and return it as a clean structured JSON object.

STRICT RULES:
- Return ONLY valid JSON. No bullet points. No markdown. No extra text.
- Extract every single detail — institute name, contact, courses, all modules with all topics, fees, eligibility, duration, tools, learning outcomes, job scope, partners, FAQs, highlights.
- For modules: list EVERY topic under each module — do not skip or summarize.
- If any field is not found in the document, set it to null. Do not use strings like "NOT FOUND".
- Never guess or invent information not present in the document.
- Ensure 'institute_name' is ALWAYS present.

JSON STRUCTURE REQUIRED:
{
  "institute_name": "string or null",
  "institute_tagline": "string or null",
  "contact": {
    "phone": "string or null",
    "email": "string or null",
    "website": "string or null",
    "address": "string or null",
    "branches": ["string"]
  },
  "courses": [
    {
      "course_name": "string",
      "fee": "string or null",
      "eligibility": "string or null",
      "duration": "string or null",
      "total_hours": "string or null",
      "mode": "string or null",
      "coordinator": "string or null",
      "partner_institute": "string or null"
    }
  ],
  "modules": [
    {
      "module_title": "string",
      "topics": ["string"]
    }
  ],
  "learning_outcomes": ["string"],
  "tools_technologies": ["string"],
  "industry_scope": ["string"],
  "job_roles": ["string"],
  "partners": ["string"],
  "highlights": ["string"],
  "faqs": [
    {
      "question": "string",
      "answer": "string"
    }
  ]
}

MAXIMIZE RECALL: List EVERY single topic mentioned. The AI agent needs this data to answer complex student queries accurately.
"""

    async def generate_pitch_script(self, context: str) -> dict:
        """
        Generates a pitch script using Gemini.
        """
        if not self.client:
            return {"sections": []}

        prompt = f"Based on this context: {context[:5000]}, generate a professional 5-part sales pitch script for an AI admissions counselor. Return as JSON with a 'sections' key containing objects with 'id', 'title', 'script', and 'instruction'."
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except:
            return {"sections": []}

ai_analysis_service = AIAnalysisService()
