"""
Investment Recommendation Tools

This module provides tools for generating personalized investment recommendations
based on a user's risk profile and portfolio analysis.
"""

from google.adk.tools.tool_context import ToolContext
from typing import Dict, List, Any

def suggest_asset_allocation(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Suggests optimal allocation across asset classes based on the user's risk profile.
    
    Returns:
        Dictionary containing suggested asset allocation percentages.
    """
    state = tool_context.state
    
    # Get risk assessment data from state
    risk_category = state.get("risk_category", {}).get("category", "Moderate")
    risk_score = state.get("risk_score", 5)
    profile = state.get("user_profile", {})
    
    # Get age for age-appropriate allocations
    age = profile.get("age", 40)
    
    # Base allocations by risk category
    allocations = {
        "Conservative": {
            "Equities": 30,
            "Fixed Income": 50,
            "Cash": 15,
            "Alternative Investments": 5
        },
        "Moderate": {
            "Equities": 50,
            "Fixed Income": 35,
            "Cash": 10,
            "Alternative Investments": 5
        },
        "Aggressive": {
            "Equities": 70,
            "Fixed Income": 20,
            "Cash": 5,
            "Alternative Investments": 5
        }
    }
    
    # Get base allocation for the risk category
    base_allocation = allocations.get(risk_category, allocations["Moderate"])
    
    # Adjust for age - older investors generally need more conservative allocations
    adjusted_allocation = base_allocation.copy()
    
    # Age-based adjustments (subtle shifts to be more conservative with age)
    if age > 60:
        # Older investors: reduce equities, increase fixed income & cash
        equity_shift = min(15, adjusted_allocation["Equities"] * 0.2)  # Reduce equities by up to 20%
        adjusted_allocation["Equities"] -= equity_shift
        adjusted_allocation["Fixed Income"] += equity_shift * 0.7  # 70% of reduction goes to fixed income
        adjusted_allocation["Cash"] += equity_shift * 0.3  # 30% of reduction goes to cash
    elif age < 30:
        # Younger investors: can take more equity risk
        fixed_income_shift = min(10, adjusted_allocation["Fixed Income"] * 0.2)  # Reduce fixed income by up to 20%
        adjusted_allocation["Fixed Income"] -= fixed_income_shift
        adjusted_allocation["Equities"] += fixed_income_shift  # Shift to equities
    
    # Format detailed equity allocation for different equity types
    equity_allocation = {}
    total_equity = adjusted_allocation["Equities"]
    
    if risk_category == "Conservative":
        equity_allocation = {
            "Large-cap stocks": round(total_equity * 0.7, 1),
            "Mid-cap stocks": round(total_equity * 0.2, 1),
            "Small-cap stocks": round(total_equity * 0.0, 1),
            "International stocks": round(total_equity * 0.1, 1)
        }
    elif risk_category == "Moderate":
        equity_allocation = {
            "Large-cap stocks": round(total_equity * 0.5, 1),
            "Mid-cap stocks": round(total_equity * 0.25, 1),
            "Small-cap stocks": round(total_equity * 0.10, 1),
            "International stocks": round(total_equity * 0.15, 1)
        }
    else:  # Aggressive
        equity_allocation = {
            "Large-cap stocks": round(total_equity * 0.40, 1),
            "Mid-cap stocks": round(total_equity * 0.25, 1),
            "Small-cap stocks": round(total_equity * 0.15, 1),
            "International stocks": round(total_equity * 0.20, 1)
        }
    
    # Save the suggested allocation to state
    state["suggested_allocation"] = {
        "main_allocation": adjusted_allocation,
        "equity_breakdown": equity_allocation
    }
    
    return {
        "status": "success",
        "risk_category": risk_category,
        "main_allocation": adjusted_allocation,
        "equity_breakdown": equity_allocation,
        "age_adjusted": age != 40
    }


def suggest_investment_products(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Recommends specific investment products based on the user's risk profile and suggested allocation.
    
    Returns:
        Dictionary containing recommended investment products by category.
    """
    state = tool_context.state
    
    # Get risk assessment and allocation data
    risk_category = state.get("risk_category", {}).get("category", "Moderate")
    allocation = state.get("suggested_allocation", {}).get("main_allocation", {})
    
    # Define product recommendations by risk profile and asset class
    recommendations = {
        "Equities": {
            "Conservative": [
                {"name": "Large Cap Index Fund", "description": "Low-cost index fund tracking large established companies"},
                {"name": "Dividend ETFs", "description": "Focused on companies with stable dividend payouts"},
                {"name": "Blue-chip stocks", "description": "Established companies with stable performance"}
            ],
            "Moderate": [
                {"name": "Index Funds (mix of large and mid-cap)", "description": "Balanced exposure to various market segments"},
                {"name": "Growth ETFs", "description": "Focus on companies with above-average growth potential"},
                {"name": "Select International Funds", "description": "Exposure to developed international markets"}
            ],
            "Aggressive": [
                {"name": "Small-cap Growth Funds", "description": "Higher growth potential with higher volatility"},
                {"name": "Sector-specific ETFs", "description": "Targeted exposure to high-growth sectors"},
                {"name": "Emerging Market Funds", "description": "Exposure to developing economies with high growth potential"}
            ]
        },
        "Fixed Income": {
            "Conservative": [
                {"name": "Government Bonds", "description": "Highest safety with lower yields"},
                {"name": "AAA Corporate Bonds", "description": "High-quality corporate debt with slightly better yields"},
                {"name": "Short-term Bond Funds", "description": "Lower interest rate risk"}
            ],
            "Moderate": [
                {"name": "Intermediate-term Bond Funds", "description": "Balance of yield and interest rate risk"},
                {"name": "Investment-grade Corporate Bond Funds", "description": "Higher yields with moderate risk"},
                {"name": "Municipal Bond Funds (tax-advantaged)", "description": "Tax benefits for certain investors"}
            ],
            "Aggressive": [
                {"name": "High-yield Corporate Bonds", "description": "Higher yields with higher default risk"},
                {"name": "Emerging Market Bonds", "description": "Higher potential returns with currency and political risk"},
                {"name": "Convertible Bonds", "description": "Potential equity upside with some downside protection"}
            ]
        },
        "Cash & Equivalents": [
            {"name": "High-yield Savings Account", "description": "Liquid savings with competitive interest rates"},
            {"name": "Money Market Funds", "description": "Short-term, high-quality investments"},
            {"name": "Short-term CDs", "description": "Fixed income for short time horizons with better rates than savings"}
        ],
        "Alternative Investments": {
            "Conservative": [
                {"name": "REITs (Real Estate Investment Trusts)", "description": "Real estate exposure with regular income"},
                {"name": "Preferred Stock ETFs", "description": "Higher dividends than common stock with less price appreciation"}
            ],
            "Moderate": [
                {"name": "Gold ETFs", "description": "Hedge against inflation and market volatility"},
                {"name": "Real Estate Funds", "description": "Broader real estate exposure across property types"}
            ],
            "Aggressive": [
                {"name": "Commodity ETFs", "description": "Exposure to various commodities for inflation protection"},
                {"name": "Private Equity Funds", "description": "Investment in private companies with higher return potential"}
            ]
        },
        "Tax-advantaged Options": [
            {"name": "401(k)/403(b)", "description": "Employer-sponsored retirement accounts with tax benefits"},
            {"name": "Traditional IRA", "description": "Tax-deferred growth for retirement"},
            {"name": "Roth IRA", "description": "Tax-free growth and withdrawals in retirement"}
        ]
    }
    
    # Build personalized recommendations based on allocation and risk profile
    personalized_recommendations = {}
    
    # Add recommendations for each asset class based on allocation percentage
    for asset_class, percentage in allocation.items():
        if asset_class == "Equities" or asset_class == "Fixed Income" or asset_class == "Alternative Investments":
            # These vary by risk profile
            personalized_recommendations[asset_class] = recommendations[asset_class][risk_category]
        elif asset_class == "Cash":
            # Cash recommendations are the same across risk profiles
            personalized_recommendations["Cash & Equivalents"] = recommendations["Cash & Equivalents"]
    
    # Always include tax-advantaged recommendations
    personalized_recommendations["Tax-advantaged Options"] = recommendations["Tax-advantaged Options"]
    
    # Save recommendations to state
    state["investment_recommendations"] = personalized_recommendations
    
    return {
        "status": "success",
        "risk_category": risk_category,
        "recommendations": personalized_recommendations
    }


def generate_risk_report(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Generates a comprehensive summary of the user's risk profile and recommendations.
    
    Returns:
        Dictionary containing the complete risk assessment report.
    """
    state = tool_context.state
    
    # Gather all relevant data from state
    profile = state.get("user_profile", {})
    risk_score = state.get("risk_score", 5)
    risk_category = state.get("risk_category", {})
    portfolio_analysis = state.get("portfolio_analysis", {})
    allocation = state.get("suggested_allocation", {})
    recommendations = state.get("investment_recommendations", {})
    
    # Extract key user information
    age = profile.get("age", "Not provided")
    income = profile.get("annual_income", "Not provided")
    expenses = profile.get("monthly_expenses", "Not provided")
    savings = profile.get("total_savings", "Not provided")
    goals = profile.get("financial_goals", "Not provided")
    self_risk = profile.get("risk_appetite", "Not provided")
    
    # Extract risk assessment details
    risk_cat = risk_category.get("category", "Moderate")
    risk_factors = risk_category.get("adjustment_factors", [])
    
    # Build comprehensive report
    report = {
        "profile_summary": {
            "age": age,
            "annual_income": f"${income:,.2f}" if isinstance(income, (int, float)) else income,
            "monthly_expenses": f"${expenses:,.2f}" if isinstance(expenses, (int, float)) else expenses,
            "total_savings": f"${savings:,.2f}" if isinstance(savings, (int, float)) else savings,
            "stated_risk_appetite": self_risk,
            "financial_goals": goals
        },
        "risk_assessment": {
            "risk_score": risk_score,
            "risk_category": risk_cat,
            "contributing_factors": risk_factors,
            "explanation": f"Your risk assessment indicates you are a {risk_cat.lower()} investor. " +
                          f"This is based on your risk score of {risk_score}/10" +
                          (f" and factors including {', '.join(risk_factors)}" if risk_factors else ".")
        },
        "portfolio_analysis": {
            "diversity_score": portfolio_analysis.get("diversity_score", "N/A"),
            "asset_count": portfolio_analysis.get("asset_count", 0),
            "asset_allocation": portfolio_analysis.get("asset_allocation", {}),
            "risk_concentration": portfolio_analysis.get("risk_concentration", "Unknown"),
            "summary": "Your current portfolio " + 
                     (f"shows {portfolio_analysis.get('risk_concentration', 'balanced')} allocation" 
                     if portfolio_analysis else "needs diversification")
        },
        "recommendations": {
            "suggested_allocation": allocation.get("main_allocation", {}),
            "equity_breakdown": allocation.get("equity_breakdown", {}),
            "suggested_products": recommendations
        }
    }
    
    # Age-specific advice
    if isinstance(age, (int, float)):
        if age < 30:
            report["age_specific_advice"] = "Given your young age, you have a longer time horizon which allows for more risk-taking and recovery from market downturns. Focus on growth."
        elif age < 45:
            report["age_specific_advice"] = "In your prime earning years, maintain a good balance between growth and stability while maximizing retirement contributions."
        elif age < 60:
            report["age_specific_advice"] = "As retirement approaches, gradually shift toward more conservative investments while still maintaining some growth components."
        else:
            report["age_specific_advice"] = "In retirement or near-retirement phase, focus on capital preservation and income generation, with a smaller allocation to growth assets."
    
    # Next steps
    report["next_steps"] = [
        "Review your current investment portfolio compared to the suggested allocation",
        "Consider tax implications before making significant changes",
        "Consult with a financial advisor for personalized advice",
        "Set up automatic contributions to maximize long-term growth",
        "Review and adjust your portfolio 1-2 times per year"
    ]
    
    # Save the complete report to state
    state["risk_report"] = report
    
    return {
        "status": "success",
        "report": report
    }