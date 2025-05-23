"""
Risk Analysis Tools

This module provides tools for analyzing financial risk tolerance,
evaluating portfolio diversification, and generating investment recommendations.
"""

from google.adk.tools.tool_context import ToolContext
from typing import Dict, List, Any

def calculate_risk_score(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Calculate a risk tolerance score (1-10) based on user profile information.
    
    A higher score indicates higher risk tolerance.
    - 1-3: Conservative investor
    - 4-6: Moderate investor
    - 7-10: Aggressive investor
    
    Returns:
        Dictionary containing the calculated risk score and factors.
    """
    state = tool_context.state
    
    # Extract user profile data from state
    profile = state.get("user_profile", {})
    age = profile.get("age", 0)
    income = profile.get("annual_income", 0)
    expenses = profile.get("monthly_expenses", 0)
    savings = profile.get("total_savings", 0)
    self_described_risk = profile.get("risk_appetite", "moderate").lower()
    
    # Initialize risk score based on self-described risk appetite
    base_score = {
        "conservative": 2,
        "moderate": 5,
        "aggressive": 8
    }.get(self_described_risk, 5)
    
    # Adjust score based on financial factors
    
    # Age factor: younger can take more risk (1-3 points)
    age_factor = 0
    if age < 30:
        age_factor = 2
    elif age < 40:
        age_factor = 1
    elif age < 50:
        age_factor = 0
    else:
        age_factor = -1
        
    # Income stability factor (0-2 points)
    monthly_income = income / 12
    income_expense_ratio = monthly_income / expenses if expenses > 0 else 1
    income_factor = min(2, max(0, int(income_expense_ratio - 2)))
    
    # Savings buffer factor (0-2 points)
    # How many months of expenses can be covered by savings
    savings_months = savings / expenses if expenses > 0 else 0
    savings_factor = 0
    if savings_months > 12:
        savings_factor = 2
    elif savings_months > 6:
        savings_factor = 1
    
    # Calculate final score
    final_score = base_score + age_factor + income_factor + savings_factor
    
    # Constrain to range 1-10
    final_score = max(1, min(10, final_score))
    
    # Store in state for other agents to access
    tool_context.state["risk_score"] = final_score
    
    # Return risk score and contributing factors
    return {
        "risk_score": final_score,
        "risk_category": "Conservative" if final_score <= 3 else 
                         "Moderate" if final_score <= 6 else 
                         "Aggressive",
        "contributing_factors": {
            "self_described_risk": self_described_risk,
            "age_factor": age_factor,
            "income_factor": income_factor,
            "savings_factor": savings_factor
        }
    }


def run_portfolio_analysis(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Analyze the diversity and risk balance of the user's investment portfolio.
    
    Returns:
        Dictionary containing portfolio analysis results.
    """
    state = tool_context.state
    
    # Get investments from state
    investments = state.get("investments", [])
    
    if not investments:
        return {
            "status": "no_data",
            "message": "No investment data available to analyze",
            "diversity_score": 0,
            "asset_allocation": {},
            "risk_concentration": "unknown"
        }
    
    # Count assets by type
    asset_counts = {}
    asset_values = {}
    total_value = 0
    
    for inv in investments:
        # Handle different possible structures of the investment object
        if isinstance(inv, dict):
            # Direct access if asset_type is at the top level
            asset_type = inv.get("asset_type")
            
            # If asset_type is not at the top level, look in details if available
            if asset_type is None and "details" in inv:
                asset_type = inv.get("details", {}).get("name", "Unknown")
                
            # If we still don't have an asset type, use a default
            if asset_type is None:
                asset_type = "Unknown"
                
            # Try to get amount from details or top level
            amount = 0
            if "details" in inv and "amount" in inv["details"]:
                amount = float(inv["details"].get("amount", 0))
            else:
                amount = float(inv.get("amount", 0))
        else:
            # Handle unexpected investment format
            asset_type = "Unknown"
            amount = 0
        
        asset_counts[asset_type] = asset_counts.get(asset_type, 0) + 1
        asset_values[asset_type] = asset_values.get(asset_type, 0) + amount
        total_value += amount
    
    # Calculate percentage allocation by asset type
    asset_allocation = {}
    if total_value > 0:
        for asset_type, value in asset_values.items():
            asset_allocation[asset_type] = round((value / total_value) * 100, 2)
    
    # Calculate diversity score (0-10)
    # More asset types and more balanced allocation scores higher
    unique_assets = len(asset_counts)
    diversity_score = min(10, unique_assets * 2)  # 2 points per asset type up to max of 10
    
    # Check for over-concentration (>50% in one asset type)
    high_concentration_assets = [asset for asset, percent in asset_allocation.items() if percent > 50]
    risk_concentration = "balanced"
    if high_concentration_assets:
        risk_concentration = f"concentrated in {', '.join(high_concentration_assets)}"
    
    # Store analysis results in state for other agents
    portfolio_analysis = {
        "diversity_score": diversity_score,
        "asset_count": len(investments),
        "unique_asset_types": unique_assets,
        "asset_allocation": asset_allocation,
        "risk_concentration": risk_concentration
    }
    
    tool_context.state["portfolio_analysis"] = portfolio_analysis
    
    return {
        "status": "success",
        **portfolio_analysis
    }


def categorize_risk_level(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Assign a risk category (Conservative/Moderate/Aggressive) based on 
    the risk score and portfolio analysis.
    
    Returns:
        Dictionary containing risk category and explanation.
    """
    state = tool_context.state
    
    # Get risk score and portfolio analysis from state
    risk_score = state.get("risk_score", 5)
    portfolio_analysis = state.get("portfolio_analysis", {})
    
    # Determine base risk category from score
    if risk_score <= 3:
        base_category = "Conservative"
    elif risk_score <= 6:
        base_category = "Moderate"
    else:
        base_category = "Aggressive"
    
    # Check for portfolio factors that might adjust category
    diversity_score = portfolio_analysis.get("diversity_score", 5)
    risk_concentration = portfolio_analysis.get("risk_concentration", "unknown")
    
    # Factors that might alter the category
    adjustment_factors = []
    final_category = base_category
    
    # Low diversity might suggest more conservative approach
    if diversity_score < 4 and base_category != "Conservative":
        adjustment_factors.append("low portfolio diversity")
        # Only adjust down one level
        if base_category == "Aggressive":
            final_category = "Moderate"
    
    # High concentration might suggest more conservative approach
    if "concentrated" in risk_concentration and base_category == "Aggressive":
        adjustment_factors.append("high concentration risk")
        final_category = "Moderate"
        
    # Store result in state
    risk_category = {
        "category": final_category,
        "base_category": base_category,
        "adjustment_factors": adjustment_factors
    }
    
    tool_context.state["risk_category"] = risk_category
    
    return risk_category