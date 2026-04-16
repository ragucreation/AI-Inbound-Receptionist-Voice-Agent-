from twilio.twiml.voice_response import VoiceResponse, Gather
from typing import Optional
import os
import uuid
import soundfile as sf
try:
    from kokoro import KPipeline
except ImportError:
    KPipeline = None

class VoiceService:
    def __init__(self):
        self.voice = os.getenv("KOKORO_VOICE", "af_heart")
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000").rstrip('/')
        self.audio_dir = "static/audio"
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # Initialize Kokoro Pipeline if available
        if KPipeline:
            try:
                self.pipeline = KPipeline(lang_code='a') 
            except Exception as e:
                print(f"Failed to initialize Kokoro: {e}")
                self.pipeline = None
        else:
            self.pipeline = None

    def _generate_audio(self, text: str) -> str:
        """Generates audio file using Kokoro and returns the filename."""
        if not self.pipeline:
            return None
        
        filename = f"{uuid.uuid4()}.wav"
        filepath = os.path.join(self.audio_dir, filename)
        
        try:
            generator = self.pipeline(text, voice=self.voice)
            # Combine all segments into one audio array
            import numpy as np
            full_audio = []
            for _, _, audio in generator:
                full_audio.append(audio)
            
            if full_audio:
                combined = np.concatenate(full_audio)
                sf.write(filepath, combined, 24000)
                return filename
        except Exception as e:
            print(f"Audio generation error: {e}")
            return None
        return None

    def get_initial_greeting(self) -> str:
        response = VoiceResponse()
        text = f"Welcome to {os.getenv('BUSINESS_NAME', 'our business')}. How can I help you today?"
        
        audio_file = self._generate_audio(text)
        
        gather = Gather(input='speech', action='/voice/handle-input', timeout=3, speech_timeout='auto')
        if audio_file:
            gather.play(f"{self.base_url}/static/audio/{audio_file}")
        else:
            gather.say(text, voice='Polly.Amy')
            
        response.append(gather)
        response.redirect('/voice/handle-input')
        return str(response)

    def generate_response_twiml(self, text: str, action: str = "collect_info") -> str:
        response = VoiceResponse()
        
        if action == "route_call":
            route_text = "Connecting you to a human agent. Please hold."
            audio_file = self._generate_audio(route_text)
            if audio_file:
                response.play(f"{self.base_url}/static/audio/{audio_file}")
            else:
                response.say(route_text, voice='Polly.Amy')
            response.dial(os.getenv("AGENT_PHONE_NUMBER", "+1234567890"))
            return str(response)

        audio_file = self._generate_audio(text)
        gather = Gather(input='speech', action='/voice/handle-input', timeout=3, speech_timeout='auto')
        
        if audio_file:
            gather.play(f"{self.base_url}/static/audio/{audio_file}")
        else:
            gather.say(text, voice='Polly.Amy')
            
        response.append(gather)
        response.append(response.redirect('/voice/handle-input'))
        return str(response)

    def generate_error_twiml(self) -> str:
        response = VoiceResponse()
        text = "I'm sorry, I'm having trouble. Please try calling again later."
        audio_file = self._generate_audio(text)
        if audio_file:
            response.play(f"{self.base_url}/static/audio/{audio_file}")
        else:
            response.say(text, voice='Polly.Amy')
        response.hangup()
        return str(response)

voice_service = VoiceService()
