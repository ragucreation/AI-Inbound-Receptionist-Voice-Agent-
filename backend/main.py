from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from .services.voice_service import voice_service
from .services.llm_service import llm_service
from .database.db import init_db, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database.models import CallLog, Lead, Appointment
import uvicorn
import os

app = FastAPI(title="AI Inbound Receptionist")

# Mount static files to serve generated audio
os.makedirs("static/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/voice", response_class=HTMLResponse)
async def voice_entry():
    """Initial call handler called by Twilio."""
    return voice_service.get_initial_greeting()

@app.post("/voice/handle-input", response_class=HTMLResponse)
async def handle_input(request: Request, db: AsyncSession = Depends(get_db)):
    """Handles speech input from Caller, processes via LLM, and returns TwiML."""
    form_data = await request.form()
    speech_result = form_data.get("SpeechResult", "")
    call_sid = form_data.get("CallSid", "")
    caller = form_data.get("From", "Unknown")

    if not speech_result:
        # If Twilio timed out or couldn't hear, prompt again or hang up
        return voice_service.generate_response_twiml("I'm sorry, I didn't catch that. Could you please say it again?")

    # 1. Process via LLM
    llm_output = await llm_service.process_interaction(speech_result)
    
    # 2. Extract Data
    intent = llm_output.get("intent", "Inquiry")
    response_text = llm_output.get("response", "I'm not sure how to help with that.")
    action = llm_output.get("action", "collect_info")
    details = llm_output.get("details", {})

    # 3. Log the interaction (In a real app, you'd update the existing call log)
    new_log = CallLog(
        call_sid=call_sid,
        caller_phone=caller,
        transcript=speech_result,
        intent=intent,
        summary=response_text,
        status="in-progress"
    )
    db.add(new_log)
    
    if intent == "Booking" and details.get("name"):
        new_lead = Lead(
            name=details.get("name"),
            phone=caller,
            service_required=details.get("service", "General"),
            interest_level="Hot"
        )
        db.add(new_lead)
    
    await db.commit()

    # 4. Generate TwiML response
    return voice_service.generate_response_twiml(response_text, action)

@app.get("/api/logs")
async def get_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CallLog).order_by(CallLog.start_time.desc()))
    return result.scalars().all()

@app.get("/api/leads")
async def get_leads(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lead).order_by(Lead.created_at.desc()))
    return result.scalars().all()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
