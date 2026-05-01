import os
import json
import pdfplumber
import docx
import re
import asyncio
from typing import List, Optional, Any, Dict
from google import genai
from google.genai import types
from app.core.config import settings

class AIAnalysisService:
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        if self.gemini_key:
            self.client = genai.Client(api_key=self.gemini_key)
            # Use 'gemini-1.5-flash' as primary, but we'll try a few variants if it fails
            self.model_name = 'gemini-1.5-flash'
        else:
            self.client = None

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
        
        # 3. ATTEMPT AI ANALYSIS WITH EXPANDED FALLBACK
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
        You are a high-precision document extraction engine specializing in educational brochures and institute prospectuses. 
        Your task is to convert the uploaded document into a structured JSON 'Neural Knowledge Base' for an AI Sales Agent.

        CRITICAL INSTRUCTIONS:
        1. EXTRACT ALL DATA: Do not summarize. If a brochure lists 20 modules, extract all 20. If each module has 15 topics, extract all 15.
        2. NO HALLUCINATIONS: Only extract what is present. If something is missing, use null or an empty list.
        3. HIGH FIDELITY: Maintain the exact terminology used in the document.
        4. JSON ONLY: Return ONLY a valid JSON object. No preamble, no markdown formatting (unless required by response_mime_type).

        SCHEMA HIERARCHY:
        - institute_name: Full legal name of the organization.
        - institute_tagline: Core value proposition or slogan.
        - contact: {phone, email, website, address, branches: []}
        - courses: Array of objects {course_name, fee, eligibility, duration, total_hours, mode, coordinator, partner_institute}.
        - modules: Array of objects {module_title, topics: []}. EXTRACT EVERY SINGLE TOPIC.
        - learning_outcomes: Array of skills the student will gain.
        - tools_technologies: List of software/tools taught (e.g. Python, AutoCAD, SAP).
        - faqs: Array of {question, answer} from the document.
        - industry_scope: Where can students work?
        - job_roles: Specific designations (e.g. Full Stack Developer).
        - partners: Hiring partners or corporate tie-ups.
        - highlights: Key selling points (e.g. 100% Placement, ISO Certified).

        MAXIMIZE RECALL: It is better to have a long list of topics than a short one. The AI agent needs this data to answer complex student queries.
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
