from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from financial_risk_assessor.agent import root_agent
from google.adk.tools.tool_context import ToolContext

app = FastAPI()

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
    # Create tool context
    tool_context = ToolContext()
    
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
    
    # Run the root agent with the formatted message
    result = await root_agent.generate_response(initial_message, tool_context)
    
    # Extract final recommendations from state
    state = tool_context.state
    risk_report = state.get("risk_report", {})
    
    return {
        "risk_assessment": risk_report.get("risk_assessment", {}),
        "portfolio_analysis": risk_report.get("portfolio_analysis", {}),
        "recommendations": risk_report.get("recommendations", {}),
        "next_steps": risk_report.get("next_steps", []),
        "age_specific_advice": risk_report.get("age_specific_advice", "")
    }