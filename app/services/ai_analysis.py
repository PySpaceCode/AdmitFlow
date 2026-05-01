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
            self.model = genai.GenerativeModel('gemini-1.5-flash')
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
        Analyzes the document using Google Gemini (Free Tier Alternative).
        """
        if not self.model:
            raise ValueError("Gemini API Key is not configured. Please get a free key from https://aistudio.google.com/")

        raw_text = await self.extract_text_from_file(file_path)
        print(f"DEBUG: Extracted text length: {len(raw_text)}")
        
        if not raw_text:
            raise ValueError("Could not extract text from the document.")

        text_context = raw_text[:30000] # Gemini has larger context, but we stay safe

        prompt = f"""
You are a highly precise document analyst. Your mission is to extract structured data from the provided BROCHURE TEXT.

TARGET DOCUMENT: {os.path.basename(file_path)}

CRITICAL CONSTRAINTS (MANDATORY):
1. **INSTITUTE IDENTITY**: Identify the REAL organization the brochure is about.
   - **DO NOT** use "AdmitFlow", "AdmissionFlow", "Admissions AI", or "AdmitFlow AI". These are the SOFTWARE PLATFORMS, not the school/company.
   - Look for headers, footers, or the "About Us" section to find the true institute name.
2. **STRICT NO-HALLUCINATION**: 
   - Only extract information explicitly mentioned in the text.
   - If a specific field (e.g., fee, duration, phone) is NOT in the text, you **MUST** return `null`.
   - **NEVER** guess or invent phone numbers, emails, or dates.
3. **CURRICULUM EXTRACTION**: 
   - List every module title and every topic mentioned.
   - If modules aren't numbered, group them logically by headers.
4. **FORMAT**: Return ONLY valid, raw JSON. No markdown blocks.

BROCHURE TEXT FOR ANALYSIS:
---
{text_context}
---

REQUIRED JSON STRUCTURE (Use `null` for missing values):
{{
  "institute_name": "string or null",
  "institute_tagline": "string or null",
  "contact": {{
    "phone": "string or null",
    "email": "string or null",
    "website": "string or null",
    "address": "string or null",
    "branches": ["string"]
  }},
  "courses": [
    {{
      "course_name": "string or null",
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
            print(f"DEBUG: Analyzing {file_path} with Gemini 1.5 Flash...")
            # Use generation_config to force JSON if supported
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.1 # Low temperature for high precision
                )
            )
            
            if not response.text:
                raise ValueError("Gemini returned an empty response.")
                
            data = json.loads(response.text)
            
            # Post-processing to clean up "fake" names if Gemini slipped up
            forbidden_names = ["admitflow", "admissionflow", "admissions ai", "admit flow"]
            name = data.get("institute_name", "")
            if name and any(f in name.lower() for f in forbidden_names):
                data["institute_name"] = "Unknown Institute"
                
            return data
        except Exception as e:
            print(f"DEBUG: Gemini/Parsing Error: {str(e)}")
            # Fallback parsing if JSON mode fails but text is returned
            try:
                text = response.text
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                return json.loads(text)
            except:
                raise ValueError(f"Gemini Analysis failed to produce valid JSON: {str(e)}")

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
