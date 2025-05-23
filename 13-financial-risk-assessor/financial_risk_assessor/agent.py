"""
Financial Risk Assessment Agent

This agent evaluates a user's financial risk profile and suggests investment strategies.
"""

from google.adk.agents import SequentialAgent
from google.adk.models.lite_llm import LiteLlm

from .subagents.collect_user_profile import collect_user_profile_agent
from .subagents.collect_investment_data import collect_investment_data_agent
from .subagents.analyze_risk_tolerance import assess_risk_profile_agent
from .subagents.generate_recommendations import generate_recommendations_agent

# Create the main sequential financial risk assessor agent
root_agent = SequentialAgent(
    name="FinancialRiskAssessor",
    description="Evaluates a user's risk profile and suggests investment strategies",
    sub_agents=[
        collect_user_profile_agent, 
        collect_investment_data_agent,
        assess_risk_profile_agent,
        generate_recommendations_agent
    ],
)