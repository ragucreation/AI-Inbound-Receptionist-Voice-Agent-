# AI Inbound Receptionist / Voice Agent 🚀

A high-impact, AI-powered voice receptionist for local businesses that automates front-desk operations.

## 🧠 Key Features
- **Real-Time Voice Interaction**: Powered by Twilio and Gemini.
- **Smart Appointment Booking**: Automated intent detection for scheduling.
- **Lead Capture**: Automatically identifies and saves high-value leads.
- **Multi-Language Support**: Handles English, Hindi, and Tamil interactions.
- **Premium Admin Dashboard**: Real-time monitoring of calls and leads.

## 🛠️ Tech Stack
- **Backend**: Python (FastAPI), SQLAlchemy (SQLite).
- **Voice**: Twilio Voice API.
- **AI**: Google Gemini (LLM), Google TTS/Polly.
- **Frontend**: React (Vite), Vanilla CSS.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js & npm
- Twilio Account + Phone Number
- Google Cloud API Key (for Gemini)

### 2. Backend Setup
1. `cd backend`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your keys.
4. `python main.py`

### 3. Frontend Setup
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### 4. Local Testing
To test the voice features locally, use `ngrok`:
`ngrok http 8000`
Then, set your Twilio Phone Number webhook (Voice) to:
`https://<your-ngrok-url>/voice`

## 📁 Project Structure
- `/backend`: FastAPI server, LLM logic, and DB models.
- `/frontend`: React dashboard with premium design.
- `/database`: SQLite storage for logs and leads.
- `/docs`: Additional documentation and design assets.
