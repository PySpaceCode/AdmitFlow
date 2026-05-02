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

        # 1. EXTRACT TEXT LOCALLY
        raw_text = await self.extract_text_from_file(file_path)
        print(f"DEBUG: Extracted {len(raw_text)} characters from {file_path}")
        
        # 2. EMERGENCY REGEX FALLBACK
        regex_data = self._extract_contact_info_fallback(raw_text)
        
        # 3. ATTEMPT NVIDIA ANALYSIS FIRST
        if self.nvidia_client and len(raw_text) > 100:
            try:
                print(f"DEBUG: Attempting analysis with NVIDIA Mistral...")
                nvidia_data = await self._analyze_with_nvidia(raw_text)
                if nvidia_data and nvidia_data.get("institute_name"):
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
        models_to_try = [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash-exp"
        ]
        
        prompt = self._get_analysis_prompt()
        
        # Read file bytes for multimodal analysis if it's a PDF
        file_bytes = None
        mime_type = None
        if file_path.lower().endswith('.pdf'):
            mime_type = "application/pdf"
        elif file_path.lower().endswith('.png') or file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
            mime_type = "image/png" if file_path.lower().endswith('.png') else "image/jpeg"

        if mime_type:
            try:
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                    print(f"DEBUG: Read {len(file_bytes)} bytes for multimodal analysis")
            except Exception as e:
                print(f"DEBUG: Error reading file bytes: {e}")
                file_bytes = None

        for model in models_to_try:
            try:
                print(f"DEBUG: Attempting analysis with model: {model}")
                
                # Instruction first for better compliance
                contents = [types.Part.from_text(text=prompt)]
                
                if file_bytes and mime_type:
                    contents.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))
                
                # Always add text content if available
                if raw_text:
                    contents.append(types.Part.from_text(text=f"RAW TEXT CONTENT:\n{raw_text[:20000]}"))

                response = self.client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.0 # Lowest temperature for maximum factuality
                    )
                )
                
                if not response.text:
                    print(f"DEBUG: Model {model} returned empty response.")
                    continue

                clean_text = response.text.strip()
                if clean_text.startswith("```json"): 
                    clean_text = clean_text[7:].split("```")[0].strip()
                elif clean_text.startswith("```"): 
                    clean_text = clean_text[3:].split("```")[0].strip()
                
                try:
                    data = json.loads(clean_text)
                except json.JSONDecodeError:
                    clean_text = re.sub(r',\s*([\]}])', r'\1', clean_text)
                    data = json.loads(clean_text)

                # Validation: if institute_name is generic or missing, it's a poor extraction
                inst_name = str(data.get("institute_name", "")).lower()
                if not inst_name or inst_name in ["null", "not found", "unknown", "analysis failed", "none"]:
                    print(f"DEBUG: Model {model} returned generic/missing institute name.")
                    continue

                data["status"] = "success"
                
                # Merge regex findings
                if not data.get("contact", {}).get("phone") and regex_data["phone"]:
                    data.setdefault("contact", {})["phone"] = regex_data["phone"]
                if not data.get("contact", {}).get("email") and regex_data["email"]:
                    data.setdefault("contact", {})["email"] = regex_data["email"]
                    
                print(f"DEBUG: Successfully extracted data using {model}")
                return self._sanitize_data(data)

            except Exception as e:
                print(f"DEBUG: Gemini Analysis Error ({model}): {str(e)}")
                continue

        # If all models failed
        print(f"CRITICAL ERROR: All Gemini models failed for {file_path}")
        fname = os.path.basename(file_path).split("_", 1)[-1] if "_" in file_path else os.path.basename(file_path)
        return self._get_fallback_data(fname, "AI failed to extract genuine data. Please check if the document is readable.", regex_data)

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
                    {"role": "system", "content": "You are a professional Data Extraction Specialist. You extract ONLY genuine, factual data from documents into valid JSON."},
                    {"role": "user", "content": f"{prompt}\n\nDOCUMENT CONTENT:\n{text[:10000]}"}
                ],
                temperature=0.1,
                top_p=1.0,
                max_tokens=2048,
                stream=False
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
            # ONLY match exact boilerplate, not descriptions containing these words
            if lowered in ["not found", "n/a", "none", "null", "not available", "unknown", "unknown institute"]:
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
You are a highly precise Data Extraction Engine for educational institutions. Your goal is to convert the provided brochure into a structured JSON database with 100% accuracy.

CRITICAL INSTRUCTIONS:
1. **ZERO HALLUCINATION**: Only extract data that is LITERALLY present in the document. Do not invent fees, dates, or contact details. Do not use any external knowledge.
2. **GENUINE ONLY**: If a field is not found in the text, you MUST set it to `null`. Do not provide generic values like "Contact us", "Unknown", or "Coming soon".
3. **EXHAUSTIVE EXTRACTION**:
   - For **Modules**: List every single chapter, unit, or topic mentioned. This is the most important part for training the AI Agent.
   - For **Courses**: Extract all variations, their duration, and specific eligibility criteria.
4. **NO PLACEHOLDERS**: If the document doesn't mention branches, "branches" should be `[]`.
5. **PITCH SUMMARY**: Create a 2-sentence summary that HIGHLIGHTS THE FACTS found in the document.

OUTPUT FORMAT (STRICT JSON):
{
  "institute_name": "Full official name",
  "institute_tagline": "Slogan (null if not found)",
  "pitch_summary": "Fact-based summary",
  "contact": {
    "phone": "Extract all found numbers",
    "email": "Extract all found emails",
    "website": "Extract official URL",
    "address": "Full physical address if found",
    "branches": ["List all branch locations mentioned"]
  },
  "courses": [
    {
      "course_name": "Full name",
      "fee": "Amount with currency (null if not found)",
      "eligibility": "Prerequisites",
      "duration": "Total time",
      "total_hours": "Number of hours if mentioned",
      "mode": "Online/Offline/Hybrid",
      "coordinator": "Name of course head"
    }
  ],
  "modules": [
    {
      "module_title": "Module Title",
      "topics": ["Exhaustive list of all sub-topics in this module"]
    }
  ],
  "learning_outcomes": ["Specific skills listed"],
  "tools_technologies": ["Software/Languages mentioned"],
  "industry_scope": ["Career growth mentions"],
  "job_roles": ["Roles listed (e.g. Developer, Analyst)"],
  "partners": ["Placement/Academic partners"],
  "highlights": ["USPs like 'Award winning', 'ISO certified', etc."],
  "faqs": [
    {
      "question": "Question from document",
      "answer": "Answer from document"
    }
  ]
}
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
