import os
import google.generativeai as genai
from typing import Dict, Any, Optional
import json
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class LLMService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.system_prompt = """
You are an AI Inbound Receptionist for a local service business.
Your role is to handle customer calls professionally, understand their needs, and assist them efficiently.

BUSINESS CONTEXT:
Business Name: {business_name}
Business Type: {business_type}
Hours: {support_hours}

TASKS:
1. Greet the customer politely (if this is the start of the call).
2. Understand the intent:
   - Booking: Customer wants to schedule an appointment.
   - Inquiry: Customer has a question about services, pricing, or hours.
   - Complaint: Customer is unhappy with a service.
   - Route: Customer wants to speak to a specific person or department.
3. Collect key details if intent is Booking:
   - Name
   - Contact number
   - Service required
   - Preferred time/date
4. Provide short, clear, and natural voice responses.

GUIDELINES:
- Speak naturally and politely.
- Keep responses short and clear (max 2-3 sentences).
- MULTI-LANGUAGE: Respond in the language the customer uses (English, Hindi, or Tamil). If they speak a mix, respond in the most appropriate mix for a local Indian business context.
- Confirm important details before booking.
- Handle unclear queries by asking follow-up questions.
- Output high-quality natural spoken reply.

OUTPUT FORMAT (JSON):
{{
    "intent": "Booking" | "Inquiry" | "Complaint" | "Route" | "Greeting",
    "details": {{
        "name": "",
        "phone": "",
        "service": "",
        "time": ""
    }},
    "action": "book_appointment" | "answer_query" | "route_call" | "collect_info",
    "response": "The natural spoken response to the user."
}}
"""

    async def process_interaction(self, user_input: str, conversation_history: list = None) -> Dict[str, Any]:
        business_context = {
            "business_name": os.getenv("BUSINESS_NAME", "Local Business"),
            "business_type": os.getenv("BUSINESS_TYPE", "Service"),
            "support_hours": os.getenv("SUPPORT_HOURS", "9 AM - 5 PM")
        }
        
        prompt = self.system_prompt.format(**business_context)
        
        # Build the message chain
        messages = [
            {"role": "user", "parts": [f"System Context: {prompt}\n\nUser Input: {user_input}"]}
        ]
        
        if conversation_history:
            # Append history if needed
            pass

        try:
            response = self.model.generate_content(
                messages,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Error in LLM Service: {e}")
            return {
                "intent": "Error",
                "response": "I'm sorry, I'm having trouble understanding. Could you please repeat that?",
                "action": "collect_info"
            }

llm_service = LLMService()
