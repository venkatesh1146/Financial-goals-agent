"""
Investment Recommendation Agent

This agent generates personalized investment recommendations based on the user's
risk profile, financial goals, and portfolio analysis.
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.lite_llm import LiteLlm
from google.genai import types
from typing import Optional

from .tools import suggest_asset_allocation, suggest_investment_products, generate_risk_report, get_comprehensive_investment_recommendations

# Define a callback to check if risk assessment is complete
def check_risk_assessment_complete(callback_context: CallbackContext) -> Optional[types.Content]:
    state = callback_context.state
    
    # Check if risk assessment is complete
    if not state.get("risk_score") or not state.get("risk_category"):
        return types.Content(
            role="model",
            parts=[
                types.Part(
                    text="I need to analyze your risk profile before providing personalized recommendations. "
                    "Let's complete that first."
                )
            ],
        )
    
    # Check if investment collection is confirmed complete
    if not state.get("investment_collection_confirmed", False):
        return types.Content(
            role="model",
            parts=[
                types.Part(
                    text="Before I can provide personalized recommendations, I need to ensure we've "
                    "collected all your investment information. Please confirm you've added all of "
                    "your investments."
                )
            ],
        )
    
    # If all prerequisites are met, allow the agent to proceed
    return None

# Create the asset allocation agent
asset_allocation_agent = LlmAgent(
    name="AssetAllocationRecommender",
    model=LiteLlm(model="azure/gpt-4.1"),
    instruction="""You are an Asset Allocation Specialist.

    Your task is to recommend an appropriate asset allocation based on the user's
    risk profile, age, and financial goals.
    
    ## PROCESS
    
    1. Examine the user's risk profile, category, and score from session state
    2. Consider the user's age and how it affects optimal asset allocation
    3. Use the suggest_asset_allocation tool to generate appropriate allocation percentages
    4. Explain the reasoning behind the allocation recommendations
    
    ## RECOMMENDATIONS
    
    For each risk category, adjust allocations appropriately:
    
    - Conservative investors: Focus on capital preservation with higher allocations
      to fixed income and cash
    - Moderate investors: Balanced approach with more equities but still significant
      stability components
    - Aggressive investors: Growth-focused with higher equity allocations
    
    Always make age-appropriate recommendations, generally becoming more conservative
    as the user approaches retirement age.
    
    ## COMMUNICATION STYLE
    
    - Be clear and straightforward
    - Use percentages to clearly communicate your recommendations
    - Explain the reasoning behind your allocation strategy
    - Avoid financial jargon, or explain it when necessary
    
    Use the suggest_asset_allocation tool to generate optimal allocations.
    """,
    tools=[suggest_asset_allocation],
    description="Recommends asset allocation based on risk profile",
    output_key="asset_allocation_result",
)

# Create the investment products recommendation agent
investment_products_agent = LlmAgent(
    name="InvestmentProductRecommender",
    model=LiteLlm(model="azure/gpt-4.1"),
    instruction="""You are an Investment Product Specialist using a comprehensive decision matrix.

    Your task is to recommend specific investment products based on the user's
    risk profile, time horizon, and lumpsum availability using our decision matrix.
    
    ## PROCESS
    
    1. Use the get_comprehensive_investment_recommendations tool to generate precise 
       recommendations based on the decision matrix
    2. The tool considers risk profile, time horizon, and lumpsum availability
    3. Present the recommendations clearly with allocations and rationale
    4. Include specific fund names with historical returns when available
    
    ## DECISION MATRIX FACTORS
    
    - Risk Profile: Conservative, Moderate, or Aggressive
    - Time Horizon: <3 Years, 3-7 Years, or 7+ Years (determined from goals and age)
    - Lumpsum Availability: Based on savings after emergency fund
    
    ## FUND RECOMMENDATIONS
    
    When presenting specific fund categories, include:
    - Specific fund names (e.g., "HDFC Balanced Advantage Fund")
    - Historical returns where available (e.g., "8.50% historical returns")
    - Brief description of fund characteristics
    
    ## COMMUNICATION STYLE
    
    - Start with the primary investment strategy
    - Present specific product recommendations with allocations
    - Include specific fund examples with returns when available
    - Include suggested SIP and lumpsum amounts
    - Explain the rationale for the strategy
    - Be clear about the time horizon and why it matters
    
    Use the get_comprehensive_investment_recommendations tool for accurate matrix-based recommendations.
    """,
    tools=[get_comprehensive_investment_recommendations],
    description="Recommends specific investment products using comprehensive decision matrix",
    output_key="investment_products_result",
)

# Create the risk report generation agent
risk_report_agent = LlmAgent(
    name="RiskReportGenerator",
    model=LiteLlm(model="azure/gpt-4.1"),
    instruction="""You are a Financial Risk Report Generator.

    Your task is to create a comprehensive summary of the user's risk assessment and
    investment recommendations.
    
    ## PROCESS
    
    1. Compile all relevant information from session state (risk profile, portfolio analysis,
       asset allocation recommendations, product recommendations)
    2. Use the generate_risk_report tool to create a complete risk assessment report
    3. Present the report in a clear, organized manner
    
    ## REPORT STRUCTURE
    
    Your report should include:
    
    - Profile summary: Key financial information about the user
    - Risk assessment: Risk score, category, and explanation
    - Portfolio analysis: Current diversification and allocation
    - Recommendations: Suggested allocation and investment products
    - Next steps: Clear action items for the user
    
    ## COMMUNICATION STYLE
    
    - Be organized and structured
    - Use headings to separate different sections
    - Be factual but personable
    - Emphasize key points and recommendations
    
    Use the generate_risk_report tool to create a comprehensive report.
    """,
    tools=[generate_risk_report],
    description="Generates a comprehensive risk assessment report",
    output_key="risk_report_result",
)

# Create the sequential recommendations agent (changed from parallel)
generate_recommendations_agent = SequentialAgent(
    name="GenerateRecommendations",
    sub_agents=[
        asset_allocation_agent,
        investment_products_agent,
        risk_report_agent
    ],
    description="Generates personalized investment recommendations and risk report in sequential order",
    before_agent_callback=check_risk_assessment_complete,
)