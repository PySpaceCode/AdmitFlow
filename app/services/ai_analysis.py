import os
import json
import pdfplumber
import docx
from typing import List, Optional
from openai import AsyncOpenAI
from app.core.config import settings

class AIAnalysisService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

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
                # Basic text file fallback
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""
            
        return text.strip()

    async def analyze_document(self, file_path: str) -> dict:
        """
        Analyzes the attached brochure/document and extracts ALL information into the strict JSON structure.
        """
        if not self.client:
            raise ValueError("OpenAI API Key is not configured")

        raw_text = await self.extract_text_from_file(file_path)
        print(f"DEBUG: Extracted text length: {len(raw_text)}")
        if not raw_text:
            print(f"DEBUG: Failed to extract text from {file_path}")
            raise ValueError("Could not extract text from the document. The file might be empty, password-protected, or contains only images without OCR.")

        # Limit text to 15k chars to fit context window and keep costs down
        text_context = raw_text[:15000]

        prompt = f"""
You are a highly accurate document analyst. Your task is to extract data from the provided BROCHURE TEXT.

TARGET DOCUMENT: {os.path.basename(file_path)}

STRICT REQUIREMENTS:
1. INSTITUTE NAME: Extract the name of the school/college/institute/company from the brochure. 
   - CRITICAL: "AdmitFlow", "AdmissionFlow", "Admissions AI", or "Admission AI" are the PLATFORM names. 
   - DO NOT use these as the institute_name unless the brochure is specifically about them.
   - If the institute name is not clearly mentioned, set it to null.
2. NO HALLUCINATION: If a piece of information (like fee, duration, phone) is not in the text, set it to null. Do not invent it.
3. FULL EXTRACTION: List EVERY single module and topic found. If there are many, include all of them.
4. VALID JSON: Return only a raw JSON object matching the schema below.

BROCHURE TEXT:
---
{text_context}
---

EXPECTED JSON SCHEMA:
{{
  "institute_name": "Exact name of the institute",
  "institute_tagline": "Tagline if found",
  "contact": {{
    "phone": "string",
    "email": "string",
    "website": "string",
    "address": "string",
    "branches": ["branch1", "branch2"]
  }},
  "courses": [
    {{
      "course_name": "string",
      "course_code": "string",
      "eligibility": "string",
      "duration": "string",
      "total_hours": "string",
      "fee": "number or string",
      "fee_note": "string",
      "mode": "string",
      "coordinator": "string",
      "partner_institute": "string"
    }}
  ],
  "modules": [
    {{
      "module_number": 1,
      "module_title": "string",
      "topics": ["topic1", "topic2"]
    }}
  ],
  "learning_outcomes": ["outcome1"],
  "tools_technologies": ["tool1"],
  "industry_scope": ["scope1"],
  "job_roles": ["role1"],
  "partners": ["partner1"],
  "accreditation": "string",
  "naac_grade": "string",
  "placement_support": "string",
  "faqs": [
    {{
      "question": "string",
      "answer": "string"
    }}
  ],
  "other_highlights": ["highlight1"]
}}
"""

        try:
            print(f"DEBUG: Sending request to OpenAI for {file_path}...")
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional educational data extractor. Output ONLY raw JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0
            )
            
            content = response.choices[0].message.content
            print("DEBUG: OpenAI Response received successfully.")
            return json.loads(content)
        except Exception as e:
            print(f"DEBUG: OpenAI/Parsing Error: {str(e)}")
            raise ValueError(f"AI Analysis failed: {str(e)}")


    async def generate_pitch_script(self, context: str) -> dict:
        """
        Uses LLM context to generate a 5-part pitch script.
        """
        if not self.client:
            # Fallback mock if no client
            return {
                "sections": [
                    {"id": 1, "title": "Opening", "script": "Hi, I'm {AgentName}...", "instruction": "Warm"}
                ]
            }

        prompt = f"Based on this context: {context[:2000]}, generate a professional 5-part sales pitch script for an AI admissions counselor. Return as JSON with a 'sections' key containing objects with 'id', 'title', 'script', and 'instruction'."
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except:
            return {"sections": []}

ai_analysis_service = AIAnalysisService()
