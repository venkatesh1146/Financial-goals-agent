from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from financial_risk_assessor.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid
import logging

# Set up logger
logger = logging.getLogger("financial_risk_assessor.api")

app = FastAPI()

# Initialize session service
session_service = InMemorySessionService()
logger.info("Initialized InMemorySessionService for API")

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
    # Log request received
    logger.info(f"Received risk analysis request for user age {profile.age}")
    
    # Create a new session with initial empty state
    app_name = "Financial_Risk_Assessor"
    user_id = f"user_{uuid.uuid4()}"
    logger.info(f"Creating new session for user_id: {user_id}")
    
    session = session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        state={}
    )
    session_id = session.id
    logger.info(f"Session created with ID: {session_id}")
    
    # Create a runner for the agent
    logger.info("Initializing agent runner")
    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )

    # Format initial message to the agent
    logger.info("Formatting user profile data for agent")
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
    
    # Process the agent's response using run_async with proper async iteration
    logger.info("Starting agent processing pipeline")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if hasattr(event, 'author') and event.author:
            logger.info(f"Agent event from: {event.author}")
        
        if event.is_final_response():
            logger.info("Received final response from agent")
            final_response = event
            # Don't break out of the loop here - allow all parallel agents to complete
        
        if event.content and event.content.parts:
            # Log intermediate responses
            part_text = event.content.parts[0].text if hasattr(event.content.parts[0], 'text') else "[non-text content]"
            # logger.info(f"Event: {part_text[:100]}...")
    
    # Get session to extract state information
    logger.info("Extracting final state from session")
    session = session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Extract final recommendations from state
    state = session.state
    risk_report = state.get("risk_report", {})
    logger.info("Constructed final risk report")
    
    response = {
        "risk_assessment": risk_report.get("risk_assessment", {}),
        "portfolio_analysis": risk_report.get("portfolio_analysis", {}),
        "recommendations": risk_report.get("recommendations", {}),
        "next_steps": risk_report.get("next_steps", []),
        "age_specific_advice": risk_report.get("age_specific_advice", "")
    }
    
    logger.info("Returning risk analysis response")
    return response