from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from financial_risk_assessor.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid

app = FastAPI()

# Initialize session service
session_service = InMemorySessionService()

class Investment(BaseModel):
    type: str  
    amount: float
    name: str
    expected_returns: Optional[float] = None
    current_value: Optional[float] = None

class UserProfile(BaseModel):
    age: int
    income: float
    expenses: float
    savings: float
    goals: str
    risk_appetite: str
    investments: List[Investment]

@app.post("/analyze")
async def analyze_risk(profile: UserProfile):
    # Create a new session with initial empty state
    app_name = "Financial_Risk_Assessor"
    user_id = f"user_{uuid.uuid4()}"
    session = session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        state={}
    )
    session_id = session.id
    
    # Create a runner for the agent
    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )

    # Format initial message to the agent
    initial_message = f"""I am {profile.age} years old, earn ${profile.income:,.2f} annually, 
    spend ${profile.expenses:,.2f} monthly, and have ${profile.savings:,.2f} in savings. 
    My financial goals are: {profile.goals}
    My risk appetite is: {profile.risk_appetite}
    
    Here are my current investments:
    """
    
    for inv in profile.investments:
        initial_message += f"\n- {inv.name}: ${inv.amount:,.2f} in {inv.type}"
        if inv.current_value:
            initial_message += f" (current value: ${inv.current_value:,.2f})"
        if inv.expected_returns:
            initial_message += f", expected returns: {inv.expected_returns}%"
    
    # Run the agent with the formatted message
    content = types.Content(role="user", parts=[types.Part(text=initial_message)])
    final_response = None
    
    # Process the agent's response
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response():
            final_response = event
    
    # Get session to extract state information
    session = session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Extract final recommendations from state
    state = session.state
    risk_report = state.get("risk_report", {})
    
    return {
        "risk_assessment": risk_report.get("risk_assessment", {}),
        "portfolio_analysis": risk_report.get("portfolio_analysis", {}),
        "recommendations": risk_report.get("recommendations", {}),
        "next_steps": risk_report.get("next_steps", []),
        "age_specific_advice": risk_report.get("age_specific_advice", "")
    }