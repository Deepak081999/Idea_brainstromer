
from core.langgraph_setup import LangGraphSetup

# Sample user input mimicking Streamlit form data
user_inputs = {
    "Idea Name": "EcoCart",
    "Purpose": "A platform to track carbon footprint of online purchases",
    "Problem": "Lack of awareness about carbon impact when shopping online",
    "Advantage": "Provides personalized eco-friendly alternatives at checkout",
    "Business Model": "Freemium model + affiliate eco-partner integration",
    "Features": "Carbon calculator, recommendation engine, browser plugin",
    "Scaling": "Expand to enterprise sustainability dashboards"
}

if __name__ == "__main__":
    print("🚀 Initializing LangGraph orchestration test...")
    orchestrator = LangGraphSetup()
    
    # Execute the flow
    response = orchestrator.execute(user_inputs)
    
    print("\n✅ Final Response from Graph:")
    print(response)