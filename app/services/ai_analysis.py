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
        if not raw_text:
            raise ValueError("Could not extract text from the document. The file might be empty or corrupted.")

        prompt = f"""
Analyze the following document text and extract ALL information into this exact JSON structure.
You are an expert document analyst for the coaching and education industry.

CRITICAL INSTRUCTIONS:
1. INSTITUTE NAME: Extract the ACTUAL institute/company name from the brochure text. DO NOT use "AdmissionFlow", "AdmitFlow", or "Admissions AI" unless it is the name of the entity described in the document. If you cannot find the name, use null.
2. SOURCE TRUTH: Only extract information present in the text. Never invent or guess details.
3. MODULES: Extract EVERY module and EVERY topic. Do not summarize. If there are 10 modules, I expect all 10 in the JSON.
4. CONTACT: Extract the specific contact details for the institute.

STRICT RULES:
- Return ONLY valid JSON. No bullet points. No markdown. No extra text.
- Extract every single detail — institute name, tagline, contact, courses, all modules with all topics, fees, eligibility, duration, tools, learning outcomes, partners, FAQs.
- For modules: list EVERY topic under each module — do not skip or summarize.
- If any field is not found in the document, set it to null.

TEXT TO ANALYZE:
{raw_text[:15000]}

EXPECTED JSON STRUCTURE:
{{
  "institute_name": null,
  "institute_tagline": null,
  "contact": {{
    "phone": null,
    "email": null,
    "website": null,
    "address": null,
    "branches": []
  }},
  "courses": [
    {{
      "course_name": null,
      "course_code": null,
      "eligibility": null,
      "duration": null,
      "total_hours": null,
      "fee": null,
      "fee_note": null,
      "mode": null,
      "coordinator": null,
      "partner_institute": null
    }}
  ],
  "modules": [
    {{
      "module_number": 1,
      "module_title": null,
      "topics": []
    }}
  ],
  "learning_outcomes": [],
  "tools_technologies": [],
  "industry_scope": [],
  "job_roles": [],
  "partners": [],
  "accreditation": null,
  "naac_grade": null,
  "placement_support": null,
  "faqs": [
    {{
      "question": null,
      "answer": null
    }}
  ],
  "other_highlights": []
}}
"""

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",  # Use gpt-4o for best extraction quality
                messages=[
                    {"role": "system", "content": "You are a specialized AI for educational document analysis. Your output must be strictly valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"OpenAI Analysis Error: {e}")
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
