from typing import Annotated, TypedDict, List, Optional, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.config import Config
from backend.app.vector_store import get_vector_store

# ----------------------------------------------------
# DATA CONTRACT VALIDATION (THE ENVELOPE)
# ----------------------------------------------------

class PropertyUIData(BaseModel):
    title: str = Field(description="The title of the real estate development (e.g., The Maldives by Bilaad).")
    location: str = Field(description="The district or location of the estate (e.g., Gwarinpa, Abuja).")
    type: str = Field(description="The class of development (e.g., Premium Eco-Villas).")
    features: List[str] = Field(description="List of key sustainability features and smart automations.")
    starting_price: str = Field(description="Starting price or flexible payment information.")
    image_url: str = Field(description="The direct image URL of the property render.")

class BilaadEnvelope(BaseModel):
    response_text: str = Field(
        description="A sophisticated, precise institutional message completely free of raw markdown formatting symbols "
                    "like double asterisks (**), single asterisks (*), hashes (#), or backticks. Highlight key pillars using "
                    "proper HTML tags like <strong>Bold Text</strong> or <li>List Item</li> instead of markdown."
    )
    ui_component: Literal["PropertyCard", "AudioBrief", "DefaultText"] = Field(
        description="The component identifier to render on the client side."
    )
    ui_data: Optional[PropertyUIData] = Field(
        None, 
        description="The structured property metadata, required if ui_component is PropertyCard."
    )

# Define Agent State matching the expected envelope
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    ui_component: Optional[str]
    ui_data: Optional[dict]
    response_text: Optional[str]

# ----------------------------------------------------
# GRAPH ROUTING LOGIC
# ----------------------------------------------------

def route_intent(state: AgentState) -> str:
    messages = state.get("messages", [])
    if not messages:
        return "rag_query"
    
    last_message = messages[-1].content.lower()
    
    # Identify keywords for custom UI rendering
    if any(keyword in last_message for keyword in ["maldives", "gwarinpa"]):
        return "maldives_card"
    elif any(keyword in last_message for keyword in ["bali island", "bali"]):
        return "bali_card"
        
    return "rag_query"

# Node 1: Handles Maldives Property Card populating (Sanitized response_text + local slider image)
def generate_maldives_card(state: AgentState) -> dict:
    return {
        "ui_component": "PropertyCard",
        "ui_data": {
            "title": "The Maldives by Bilaad",
            "location": "Gwarinpa, Abuja",
            "type": "Premium Eco-Villas",
            "features": [
                "Smart Automation",
                "Solar Grid Integration",
                "Waste-to-Energy Systems",
                "Luxury Green Spaces"
            ],
            "starting_price": "Premium Installments Available",
            "image_url": "https://www.bilaadnigeria.com/wp-content/uploads/slider/cache/0f862d0857574a9372b070b1333a3d3a/CAPRI-scaled.jpg"
        },
        "response_text": "Introducing <strong>The Maldives by Bilaad</strong>, our signature sustainable eco-villa residential development in Gwarinpa, Abuja. This premium community is designed to lower energy consumption by integrating solar grid tech, advanced water recycling, and smart home systems. Please review the detailed property presentation card on the side panel."
    }

# Node 2: Handles Bali Island Property Card populating (Sanitized response_text + local slider image)
def generate_bali_card(state: AgentState) -> dict:
    return {
        "ui_component": "PropertyCard",
        "ui_data": {
            "title": "The Bali Island by Bilaad",
            "location": "Life Camp, Abuja",
            "type": "Luxury Resort Residences",
            "features": [
                "Resort-Inspired Architecture",
                "Greywater Recycling",
                "Solar Streetlighting",
                "Energy-Efficient Materials"
            ],
            "starting_price": "Premium Installments Available",
            "image_url": "https://www.bilaadnigeria.com/wp-content/uploads/slider/cache/f5b8f97f3525a08c84dcc86190b669e9/THE-BAHAMAS_18-Photo-scaled.jpg"
        },
        "response_text": "Presenting <strong>The Bali Island by Bilaad</strong>, an premium resort-living development located in Life Camp, Abuja. Built with environment-friendly materials and incorporating greywater irrigation systems, it offers a peaceful green sanctuary in the capital. View the highlights in the property specification panel."
    }

# Node 3: General RAG search and structured generation
def execute_rag_query(state: AgentState) -> dict:
    messages = state.get("messages", [])
    query = messages[-1].content if messages else ""
    
    v_store = get_vector_store()
    context = ""
    
    if v_store:
        try:
            docs = v_store.similarity_search(query, k=3)
            context = "\n\n".join([f"Source: {d.metadata.get('title', 'Unknown')}\nContent: {d.page_content}" for d in docs])
        except Exception as e:
            print(f"[WARNING] Vector store search error: {e}")
            context = "No database documents retrieved."
            
    system_prompt = (
        "You are Bilaad AI, a sophisticated, precise institutional real estate investment advisor for Bilaad Nigeria.\n"
        "Your tone must be elite, professional, precise, and investor-focused. Avoid conversational fluff or greeting tags.\n"
        "CRITICAL: Do NOT use raw markdown formatting symbols (such as **bold**, *italics*, # headers, or lists with *). "
        "To bold key phrases, use <strong>Text</strong>. For lists, use <li>Item</li> tags. All responses must be "
        "clean text or standard HTML markup inside the response_text field.\n\n"
        f"Context from Bilaad Portfolio:\n{context}"
    )
    
    if Config.GEMINI_API_KEY:
        try:
            # Initialize ChatGoogleGenerativeAI with structured output parsing
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash", 
                google_api_key=Config.GEMINI_API_KEY,
                temperature=0.2
            )
            
            # Format conversational history
            llm_messages = [{"role": "system", "content": system_prompt}]
            for msg in messages:
                role = "user" if isinstance(msg, HumanMessage) else "assistant"
                llm_messages.append({"role": role, "content": msg.content})
                
            # Request structured envelope validation directly from Gemini
            structured_llm = llm.with_structured_output(BilaadEnvelope)
            envelope = structured_llm.invoke(llm_messages)
            
            return {
                "ui_component": envelope.ui_component,
                "ui_data": envelope.ui_data.model_dump() if envelope.ui_data else None,
                "response_text": envelope.response_text
            }
        except Exception as e:
            print(f"[ERROR] Structured LLM error: {e}")
            err_msg = str(e)
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                friendly_msg = "I apologize, but the reasoning engine is currently receiving a high volume of requests. Please wait a brief moment before sending your next message."
            else:
                friendly_msg = "I apologize, but the connection to our services timed out. Please try again in a few moments."
            
            return {
                "ui_component": "DefaultText",
                "ui_data": None,
                "response_text": friendly_msg
            }
    else:
        # High-class offline fallback envelope
        return {
            "ui_component": "DefaultText",
            "ui_data": None,
            "response_text": "Bilaad AI is currently running in offline fallback mode. Bilaad Nigeria specializes in sustainable real estate developments in Abuja, focusing on smart home automation, energy-efficient building materials, and greywater recycling. Please configure the <strong>GEMINI_API_KEY</strong> environment variable to unlock full interactive conversation capabilities."
        }

# ----------------------------------------------------
# STATE GRAPH COMPILATION
# ----------------------------------------------------

workflow = StateGraph(AgentState)

workflow.add_node("maldives_card", generate_maldives_card)
workflow.add_node("bali_card", generate_bali_card)
workflow.add_node("rag_query", execute_rag_query)

workflow.add_conditional_edges(
    START,
    route_intent,
    {
        "maldives_card": "maldives_card",
        "bali_card": "bali_card",
        "rag_query": "rag_query"
    }
)

workflow.add_edge("maldives_card", END)
workflow.add_edge("bali_card", END)
workflow.add_edge("rag_query", END)

agent_app = workflow.compile()
