import os
import json
import pdfplumber
import docx
from typing import List, Optional
import google.generativeai as genai
from app.core.config import settings

class AIAnalysisService:
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

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
        Analyzes the document using Google Gemini with native PDF/multimodal support.
        """
        if not self.model:
            raise ValueError("Gemini API Key is not configured. Please get a key from https://aistudio.google.com/")

        extension = os.path.splitext(file_path)[1].lower()
        
        # Prepare the prompt
        prompt = f"""
You are a highly precise document analyst. Your mission is to extract structured data from the provided document.

CRITICAL CONSTRAINTS (MANDATORY):
1. **INSTITUTE IDENTITY**: Identify the REAL organization the document is about.
   - **DO NOT** use "AdmitFlow", "AdmissionFlow", "Admissions AI", or "AdmitFlow AI". These are the platform names.
   - Look for logos, headers, or "About Us" to find the true institute name.
2. **STRICT NO-HALLUCINATION**: 
   - Only extract information explicitly mentioned.
   - If a specific field is NOT in the text, you **MUST** return `null`.
   - **NEVER** invent phone numbers or emails.
3. **FORMAT**: Return ONLY valid, raw JSON. No markdown blocks.

REQUIRED JSON STRUCTURE (Use `null` for missing values):
{{
  "institute_name": "string (MANDATORY: Look for headers, logos, footer text)",
  "institute_tagline": "string or null",
  "contact": {{
    "phone": "string or null (Extract ALL phone numbers found)",
    "email": "string or null (Extract ALL emails found)",
    "website": "string or null",
    "address": "string or null",
    "branches": ["string"]
  }},
  "courses": [
    {{
      "course_name": "string",
      "course_code": "string or null",
      "eligibility": "string or null",
      "duration": "string or null",
      "total_hours": "string or null",
      "fee": "number or string or null",
      "fee_note": "string or null",
      "mode": "string or null",
      "coordinator": "string or null",
      "partner_institute": "string or null"
    }}
  ],
  "modules": [
    {{
      "module_number": "number",
      "module_title": "string",
      "topics": ["string"]
    }}
  ],
  "learning_outcomes": ["string"],
  "tools_technologies": ["string"],
  "industry_scope": ["string"],
  "job_roles": ["string"],
  "partners": ["string"],
  "accreditation": "string or null",
  "naac_grade": "string or null",
  "placement_support": "string or null",
  "faqs": [
    {{
      "question": "string",
      "answer": "string"
    }}
  ],
  "other_highlights": ["string"]
}}
"""

        try:
            print(f"DEBUG: Uploading {file_path} to Gemini...")
            
            # Use native PDF support for Gemini 1.5
            if extension == ".pdf":
                # Upload file to Gemini File API
                uploaded_file = genai.upload_file(path=file_path)
                print(f"DEBUG: File uploaded: {uploaded_file.name}")
                
                response = self.model.generate_content(
                    [uploaded_file, prompt],
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                )
                
                # Cleanup: Files are deleted after 48h, but we can't easily delete here without more logic
                # For high-volume production, we should track and delete.
            else:
                # Fallback for DOCX or others where we extract text first
                raw_text = await self.extract_text_from_file(file_path)
                if not raw_text:
                    raise ValueError("Could not extract text from the document.")
                
                response = self.model.generate_content(
                    f"{prompt}\n\nDOCUMENT TEXT:\n{raw_text[:30000]}",
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")
            
            # Clean up potential markdown formatting in response
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:-3].strip()
            elif clean_text.startswith("```"):
                clean_text = clean_text[3:-3].strip()
                
            data = json.loads(clean_text)
            
            # Post-processing to clean up "fake" names and ensure structure
            forbidden_names = ["admitflow", "admissionflow", "admissions ai", "admit flow", "university system", "sample"]
            name = data.get("institute_name", "")
            if not name or any(f in name.lower() for f in forbidden_names):
                # Try to find a better name if it failed
                data["institute_name"] = "Document Under Analysis"
                
            # Ensure critical lists exist so frontend doesn't crash
            for key in ["courses", "modules", "learning_outcomes", "tools_technologies", "faqs"]:
                if key not in data or data[key] is None:
                    data[key] = []
            
            if "contact" not in data or data["contact"] is None:
                data["contact"] = {"phone": None, "email": None, "website": None, "address": None, "branches": []}

            return data
            
        except Exception as e:
            print(f"DEBUG: Gemini Analysis Error: {str(e)}")
            # Last ditch effort: try extracting text and sending it normally if native PDF failed
            try:
                raw_text = await self.extract_text_from_file(file_path)
                if raw_text:
                    response = self.model.generate_content(
                        f"{prompt}\n\nDOCUMENT TEXT:\n{raw_text[:20000]}",
                        generation_config=genai.types.GenerationConfig(
                            response_mime_type="application/json",
                            temperature=0.1
                        )
                    )
                    return json.loads(response.text)
            except:
                pass
            raise ValueError(f"AI Analysis failed: {str(e)}")


    async def generate_pitch_script(self, context: str) -> dict:
        """
        Generates a pitch script using Gemini.
        """
        if not self.model:
            return {"sections": []}

        prompt = f"Based on this context: {context[:5000]}, generate a professional 5-part sales pitch script for an AI admissions counselor. Return as JSON with a 'sections' key containing objects with 'id', 'title', 'script', and 'instruction'."
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except:
            return {"sections": []}

ai_analysis_service = AIAnalysisService()
