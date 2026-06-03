import os
import sys

# Add backend project parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_core.messages import HumanMessage
from backend.app.agent import agent_app

def run_tests():
    print("[TESTS] Starting LangGraph Routing & Intent Tests...")
    
    tests = [
        {
            "name": "Maldives Intent Routing",
            "query": "Tell me about the Maldives project in Gwarinpa",
            "expected_ui": "PropertyCard",
            "expected_title": "The Maldives by Bilaad"
        },
        {
            "name": "Bali Island Intent Routing",
            "query": "Can I see details on Bali Island?",
            "expected_ui": "PropertyCard",
            "expected_title": "The Bali Island by Bilaad"
        },
        {
            "name": "General Query (RAG Routing)",
            "query": "What are Bilaad's main sustainable goals?",
            "expected_ui": "DefaultText",
            "expected_title": None
        }
    ]
    
    success = True
    for t in tests:
        print(f"\n[RUN] {t['name']}")
        print(f"   Query: '{t['query']}'")
        
        state = {
            "messages": [HumanMessage(content=t["query"])],
            "ui_component": None,
            "ui_data": None,
            "response_text": None
        }
        
        output = agent_app.invoke(state)
        ui_comp = output.get("ui_component")
        ui_data = output.get("ui_data")
        resp_text = output.get("response_text")
        
        # Verify UI component
        if ui_comp != t["expected_ui"]:
            print(f"[FAIL] Expected ui_component '{t['expected_ui']}', got '{ui_comp}'")
            success = False
            continue
            
        # Verify UI Data title if expected
        if t["expected_title"]:
            if not ui_data or ui_data.get("title") != t["expected_title"]:
                print(f"[FAIL] Expected ui_data title '{t['expected_title']}', got '{ui_data.get('title') if ui_data else None}'")
                success = False
                continue
                
        print(f"[SUCCESS] Response preview: '{resp_text[:60]}...'")
        if ui_comp:
            print(f"   Component Rendered: {ui_comp} | Data: {ui_data}")
            
    if success:
        print("\n[SUCCESS] All LangGraph routing tests passed successfully!")
        sys.exit(0)
    else:
        print("\n[FAIL] Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
