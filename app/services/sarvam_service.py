from typing import Optional
from app.core.config import settings

class SarvamService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.SARVAM_API_KEY

    async def get_stt(self, audio_content: bytes) -> str:
        # Mock Sarvam STT
        if not self.api_key:
            return "Mock: User said they want to join Computer Science."
        # Placeholder for real API call
        return "Transcribed audio via Sarvam."

    async def get_tts(self, text: str) -> bytes:
        # Mock Sarvam TTS
        if not self.api_key:
            return b"mock_audio_content"
        # Placeholder for real API call
        return b"voice_audio_content"

sarvam_service = SarvamService()
