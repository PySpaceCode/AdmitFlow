import os
import json
import pdfplumber
import docx
import re
from typing import List, Optional
from google import genai
from google.genai import types
from app.core.config import settings

class AIAnalysisService:
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        if self.gemini_key:
            self.client = genai.Client(api_key=self.gemini_key)
            self.model_name = 'gemini-flash-latest'
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
        Analyzes the document using a robust text-first approach to avoid File API errors.
        """
        if not self.client:
            raise ValueError("Gemini API Key is not configured.")

        # 1. EXTRACT TEXT LOCALLY (Most reliable)
        raw_text = await self.extract_text_from_file(file_path)
        
        # 2. EMERGENCY REGEX FALLBACK (Pre-parsing important info)
        regex_data = self._extract_contact_info_fallback(raw_text)
        
        if not raw_text:
            # Try to get at least the filename as a name
            fname = os.path.basename(file_path).replace("_", " ")
            return self._get_fallback_data(fname, "Could not read document text.", regex_data)

        # 3. ATTEMPT AI ANALYSIS
        try:
            # Prepare a clean prompt with the raw text
            prompt = self._get_analysis_prompt()
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{prompt}\n\nDOCUMENT CONTENT:\n{raw_text[:25000]}", # Limit to avoid token issues
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            
            if not response.text:
                raise ValueError("Empty AI response")

            clean_text = response.text.strip()
            # Clean markdown code blocks if present
            if clean_text.startswith("```json"): clean_text = clean_text[7:-3].strip()
            elif clean_text.startswith("```"): clean_text = clean_text[3:-3].strip()
            
            data = json.loads(clean_text)
            
            # Merge regex findings if AI missed them
            if not data.get("contact", {}).get("phone") and regex_data["phone"]:
                data.setdefault("contact", {})["phone"] = regex_data["phone"]
            if not data.get("contact", {}).get("email") and regex_data["email"]:
                data.setdefault("contact", {})["email"] = regex_data["email"]
                
            return data

        except Exception as e:
            print(f"Gemini Analysis Error: {str(e)}")
            fname = os.path.basename(file_path).split("_", 1)[-1] if "_" in file_path else os.path.basename(file_path)
            return self._get_fallback_data(fname, f"AI Analysis failed: {str(e)}", regex_data)

    def _extract_contact_info_fallback(self, text: str) -> dict:
        """Uses Regex to find email and phone if AI fails."""
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        phones = re.findall(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        
        return {
            "email": emails[0] if emails else None,
            "phone": phones[0] if phones else None
        }

    def _get_fallback_data(self, name: str, error_msg: str, regex_data: dict = None) -> dict:
        """Returns a safe data structure when analysis fails."""
        return {
            "institute_name": name or "Unknown Institute",
            "institute_tagline": "Data extracted via fallback",
            "status": "partial",
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
            "faqs": [],
            "error_detail": error_msg
        }

    def _get_analysis_prompt(self) -> str:
        return """
        EXTRACT ALL DETAILS from the following university/institute brochure.
        You MUST return the data in the following JSON format ONLY. 
        Be thorough. If you can't find a field, use null.
        
        REQUIRED JSON STRUCTURE:
        {
          "institute_name": "string (Look for headers, logos, footer text)",
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
              "duration": "string or null",
              "eligibility": "string or null",
              "fees": "string or null",
              "description": "string or null"
            }
          ],
          "modules": [
            {
              "course_name": "string",
              "module_title": "string",
              "topics": ["string"]
            }
          ],
          "learning_outcomes": ["string"],
          "tools_technologies": ["string"],
          "faqs": [
            {
              "question": "string",
              "answer": "string"
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
