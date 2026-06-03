from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage

from backend.app.graph import agent_app
from backend.app.scraper import ingest_portfolio_data
from backend.app.config import Config, IS_CONFIGURED

app = FastAPI(
    title="Bilaad AI API",
    description="Luxury Investor Real Estate RAG Assistant API",
    version="1.0.0"
)

# Enable CORS for Next.js app communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageModel(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[MessageModel] = []

class ChatResponse(BaseModel):
    response_text: str
    ui_component: Optional[str] = None
    ui_data: Optional[Dict[str, Any]] = None

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "supabase_configured": IS_CONFIGURED,
        "gemini_api_configured": bool(Config.GEMINI_API_KEY)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Convert history to LangChain messages
        langchain_messages = []
        for msg in request.history:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
                
        # Append latest user message
        langchain_messages.append(HumanMessage(content=request.message))
        
        # Invoke LangGraph app state
        initial_state = {
            "messages": langchain_messages,
            "ui_component": None,
            "ui_data": None,
            "response_text": None
        }
        
        output = agent_app.invoke(initial_state)
        
        return ChatResponse(
            response_text=output.get("response_text", "No response generated."),
            ui_component=output.get("ui_component"),
            ui_data=output.get("ui_data")
        )
    except Exception as e:
        print(f"[ERROR] Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def trigger_ingestion():
    result = ingest_portfolio_data()
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
