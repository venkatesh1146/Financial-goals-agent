"""
Risk Profile Assessment Agent

This agent uses parallel processing to assess a user's risk tolerance based on their 
financial profile, investment history, and stated preferences.
"""

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from typing import Optional

from .tools import calculate_risk_score, run_portfolio_analysis, categorize_risk_level

# Define a callback to check if investment collection is complete
def check_investment_collection(callback_context: CallbackContext) -> Optional[types.Content]:
    state = callback_context.state
    
    # Check if investment collection is explicitly confirmed complete
    if not state.get("investment_collection_confirmed", False):
        investments = state.get("investments", [])
        
        if not investments:
            # No investments recorded at all
            return types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="Before I can complete your risk assessment, I need information about your investments. "
                        "Let's continue with collecting your investment data.\n\n"
                        "What types of investments do you currently have? For example:\n"
                        "- Stocks\n"
                        "- Bonds\n"
                        "- Real Estate\n"
                        "- Retirement Accounts\n"
                        "- Cash or Savings\n"
                        "- Or any other assets"
                    )
                ],
            )
        else:
            # Has some investments but hasn't confirmed completion
            return types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="I see you've added " + str(len(investments)) + " investment(s) so far. "
                        "Before I proceed with your risk assessment, I need to confirm:\n\n"
                        "Do you have any more investments or assets to add? "
                        "It's important that I have a complete picture of your portfolio to provide accurate recommendations."
                    )
                ],
            )
    
    # If investment collection is confirmed complete, allow the agent to proceed
    return None

# Create the risk scoring agent
risk_score_agent = LlmAgent(
    name="RiskScoreCalculator",
    model=LiteLlm(model="azure/gpt-4.1"),
    instruction="""You are a Financial Risk Score Calculator.

    Your task is to calculate a numerical risk score for the user based on their
    financial profile and stated preferences.
    
    ## PROCESS
    
    1. Review the user's financial profile (age, income, savings, goals, risk appetite)
    2. Use the calculate_risk_score tool to generate a quantitative risk assessment
    3. Store the risk score in the session state for other agents to use
    
    ## COMMUNICATION STYLE
    
    - Be brief and factual
    - Explain the key factors that influenced the risk score
    - Put the score in context (what does it mean for the user)
    
    Use the calculate_risk_score tool to perform accurate risk calculations.
    """,
    tools=[calculate_risk_score],
    description="Calculates a numerical risk score based on user profile",
    output_key="risk_score_result",
)

# Create the portfolio analysis agent
portfolio_analysis_agent = LlmAgent(
    name="PortfolioAnalyzer",
    model=LiteLlm(model="azure/gpt-4.1"),
    instruction="""You are a Portfolio Analysis Specialist.

    Your task is to analyze the user's investment portfolio for diversification,
    asset allocation, and concentration risk.
    
    ## PROCESS
    
    1. Examine the user's current investment portfolio from session state
    2. Use the run_portfolio_analysis tool to assess diversification and allocation
    3. Identify potential areas of concern (over-concentration, inappropriate risk levels)
    4. Store your analysis results in session state
    
    ## COMMUNICATION STYLE
    
    - Be analytical but clear
    - Use percentages and proportions to illustrate portfolio composition
    - Highlight any significant risks or imbalances
    
    Use the run_portfolio_analysis tool to perform accurate portfolio assessment.
    """,
    tools=[run_portfolio_analysis],
    description="Analyzes portfolio diversification and allocation",
    output_key="portfolio_analysis_result",
)

# Create the risk categorization agent
risk_categorization_agent = LlmAgent(
    name="RiskCategorizer",
    model=LiteLlm(model="azure/gpt-4.1"),
    instruction="""You are a Financial Risk Categorization Specialist.

    Your task is to assign a risk category to the user based on their risk score
    and portfolio analysis.
    
    ## PROCESS
    
    1. Review the user's risk score and portfolio analysis from session state
    2. Use the categorize_risk_level tool to determine the appropriate risk category
    3. Store the risk category in session state
    
    ## RISK CATEGORIES
    
    - Conservative: Focus on capital preservation, minimal volatility
    - Moderate: Balanced approach with some growth and some stability
    - Aggressive: Focus on growth, comfortable with higher volatility
    
    ## COMMUNICATION STYLE
    
    - Be clear and straightforward
    - Explain why the user fits into their assigned category
    - Be factual and avoid judgmental language
    
    Use the categorize_risk_level tool to ensure accurate categorization.
    """,
    tools=[categorize_risk_level],
    description="Assigns a risk category based on score and analysis",
    output_key="risk_category_result",
)

# Create the parallel risk assessment agent
assess_risk_profile_agent = ParallelAgent(
    name="AssessRiskProfile",
    sub_agents=[
        risk_score_agent,
        portfolio_analysis_agent,
        risk_categorization_agent
    ],
    description="Calculates risk score, analyzes portfolio, and categorizes risk level in parallel",
    before_agent_callback=check_investment_collection,
)