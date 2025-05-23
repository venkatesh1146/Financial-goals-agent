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
            "Large-cap MF Equity": round(total_equity * 0.7, 1),
            "Mid-cap MF Equity": round(total_equity * 0.2, 1),
            "Small-cap MF Equity": round(total_equity * 0.0, 1),
            "International MF Equity": round(total_equity * 0.1, 1)
        }
    elif risk_category == "Moderate":
        equity_allocation = {
            "Large-cap MF Equity": round(total_equity * 0.5, 1),
            "Mid-cap MF Equity": round(total_equity * 0.25, 1),
            "Small-cap MF Equity": round(total_equity * 0.10, 1),
            "International MF Equity": round(total_equity * 0.15, 1)
        }
    else:  # Aggressive
        equity_allocation = {
            "Large-cap MF Equity": round(total_equity * 0.40, 1),
            "Mid-cap MF Equity": round(total_equity * 0.25, 1),
            "Small-cap MF Equity": round(total_equity * 0.15, 1),
            "International MF Equity": round(total_equity * 0.20, 1)
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
    comprehensive_recommendations = state.get("comprehensive_recommendations", {})
    
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
        "comprehensive_recommendations": comprehensive_recommendations,
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
    
    # Enhanced next steps with comprehensive recommendations
    next_steps = [
        "Review your current investment portfolio compared to the suggested allocation",
        "Consider tax implications before making significant changes",
        "Consult with a financial advisor for personalized advice",
        "Set up automatic contributions to maximize long-term growth",
        "Review and adjust your portfolio 1-2 times per year"
    ]
    
    # Add specific next steps based on comprehensive recommendations
    if comprehensive_recommendations:
        if comprehensive_recommendations.get("suggested_sip_amount", 0) > 0:
            sip_amount = comprehensive_recommendations.get("suggested_sip_amount", 0)
            next_steps.insert(0, f"Start a SIP of ₹{sip_amount:,.0f} per month based on your income")
        
        if comprehensive_recommendations.get("suggested_lumpsum_amount", 0) > 0:
            lumpsum_amount = comprehensive_recommendations.get("suggested_lumpsum_amount", 0)
            next_steps.insert(1, f"Consider investing ₹{lumpsum_amount:,.0f} as lumpsum while maintaining emergency fund")
        
        primary_strategy = comprehensive_recommendations.get("primary_strategy", "")
        if primary_strategy:
            next_steps.insert(2, f"Focus on {primary_strategy.lower()} as your primary investment strategy")
    
    report["next_steps"] = next_steps
    
    # Save the complete report to state
    state["risk_report"] = report
    
    return {
        "status": "success",
        "report": report
    }


def get_comprehensive_investment_recommendations(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Provides comprehensive investment recommendations based on risk profile, 
    time horizon, and lumpsum availability using a decision matrix approach.
    
    Returns:
        Dictionary containing specific investment recommendations based on the decision matrix.
    """
    state = tool_context.state
    
    # Get user data from state
    profile = state.get("user_profile", {})
    risk_category = state.get("risk_category", {}).get("category", "Moderate")
    
    # Extract relevant parameters
    age = profile.get("age", 40)
    goals = profile.get("financial_goals", "")
    total_savings = profile.get("total_savings", 0)
    monthly_income = profile.get("annual_income", 0) / 12 if profile.get("annual_income") else 0
    
    # Determine time horizon based on goals and age
    time_horizon = determine_time_horizon(goals, age)
    
    # Determine lumpsum availability (assume available if savings > 6 months expenses)
    monthly_expenses = profile.get("monthly_expenses", 0)
    emergency_fund_needed = monthly_expenses * 6
    lumpsum_available = total_savings > emergency_fund_needed
    
    # Investment recommendation matrix based on the provided table
    recommendations_matrix = {
        "Conservative": {
            "< 3 Years": {
                "lumpsum_yes": {
                    "primary": "FD (Lumpsum)",
                    "products": [
                        {"name": "Fixed Deposits", "allocation": 70, "description": "Secure fixed returns for short-term goals", "funds": get_specific_fund_recommendations("Conservative", "FD")},
                        {"name": "Liquid Funds", "allocation": 20, "description": "Easy access with stable returns"},
                        {"name": "Ultra Short-term Funds", "allocation": 10, "description": "Slightly higher returns than savings"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "FD (SIP if possible)",
                    "products": [
                        {"name": "Monthly FD SIP", "allocation": 60, "description": "Regular fixed deposit investments", "funds": get_specific_fund_recommendations("Conservative", "FD")},
                        {"name": "Liquid Fund SIP", "allocation": 30, "description": "Systematic liquid fund investments"},
                        {"name": "Savings Account", "allocation": 10, "description": "Emergency liquidity"}
                    ]
                }
            },
            "3-7 Years": {
                "lumpsum_yes": {
                    "primary": "FD + Short-term Debt MF (Lumpsum + SIP)",
                    "products": [
                        {"name": "Fixed Deposits", "allocation": 40, "description": "Stable foundation for medium-term goals", "funds": get_specific_fund_recommendations("Conservative", "FD")},
                        {"name": "Short-term Debt Mutual Funds", "allocation": 35, "description": "Better returns than FDs with moderate risk", "funds": get_specific_fund_recommendations("Conservative", "Short-term Debt MF")},
                        {"name": "Conservative Hybrid Funds", "allocation": 20, "description": "Balanced debt-equity exposure", "funds": get_specific_fund_recommendations("Conservative", "Conservative Hybrid MF")},
                        {"name": "Liquid Funds", "allocation": 5, "description": "Emergency liquidity"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "SIP in Short-term Debt / Conservative Hybrid MF",
                    "products": [
                        {"name": "Short-term Debt Fund SIP", "allocation": 50, "description": "Systematic debt fund investments", "funds": get_specific_fund_recommendations("Conservative", "Short-term Debt MF")},
                        {"name": "Conservative Hybrid Fund SIP", "allocation": 30, "description": "Balanced approach with SIP", "funds": get_specific_fund_recommendations("Conservative", "Conservative Hybrid MF")},
                        {"name": "Monthly FD", "allocation": 20, "description": "Fixed component for stability", "funds": get_specific_fund_recommendations("Conservative", "FD")}
                    ]
                }
            },
            "7+ Years": {
                "lumpsum_yes": {
                    "primary": "FD + Conservative Hybrid MF (Lumpsum + SIP)",
                    "products": [
                        {"name": "Conservative Hybrid Mutual Funds", "allocation": 45, "description": "Long-term balanced growth with capital protection", "funds": get_specific_fund_recommendations("Conservative", "Conservative Hybrid MF")},
                        {"name": "ELSS (Tax Saving)", "allocation": 25, "description": "Tax benefits with equity exposure"},
                        {"name": "Fixed Deposits", "allocation": 20, "description": "Stable income component", "funds": get_specific_fund_recommendations("Conservative", "FD")},
                        {"name": "PPF/EPF", "allocation": 10, "description": "Long-term tax-free returns"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "SIP in Debt Hybrid / Conservative Hybrid MF",
                    "products": [
                        {"name": "Conservative Hybrid Fund SIP", "allocation": 50, "description": "Systematic balanced investments", "funds": get_specific_fund_recommendations("Conservative", "Conservative Hybrid MF")},
                        {"name": "ELSS SIP", "allocation": 30, "description": "Tax-saving equity exposure"},
                        {"name": "PPF", "allocation": 20, "description": "Long-term guaranteed returns"}
                    ]
                }
            }
        },
        "Moderate": {
            "< 3 Years": {
                "lumpsum_yes": {
                    "primary": "FD + Arbitrage / Low Duration Debt MF (Lumpsum)",
                    "products": [
                        {"name": "Fixed Deposits", "allocation": 50, "description": "Capital protection for short-term needs", "funds": get_specific_fund_recommendations("Moderate", "FD")},
                        {"name": "Arbitrage Funds", "allocation": 30, "description": "Equity taxation with debt-like returns", "funds": get_specific_fund_recommendations("Moderate", "Arbitrage / Low Duration Debt MF")},
                        {"name": "Low Duration Debt Funds", "allocation": 15, "description": "Enhanced returns with low interest rate risk"},
                        {"name": "Liquid Funds", "allocation": 5, "description": "Immediate liquidity"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "FD only, avoid equity SIP <3yrs",
                    "products": [
                        {"name": "Monthly FD", "allocation": 70, "description": "Regular fixed deposits for capital safety", "funds": get_specific_fund_recommendations("Moderate", "FD")},
                        {"name": "Ultra Short-term Fund SIP", "allocation": 25, "description": "Slightly enhanced returns"},
                        {"name": "Liquid Fund", "allocation": 5, "description": "Emergency access"}
                    ]
                }
            },
            "3-7 Years": {
                "lumpsum_yes": {
                    "primary": "Balanced Advantage MF + ELSS + FD (Lumpsum + SIP)",
                    "products": [
                        {"name": "Balanced Advantage Funds", "allocation": 40, "description": "Dynamic asset allocation based on market conditions", "funds": get_specific_fund_recommendations("Moderate", "Balanced Advantage MF")},
                        {"name": "ELSS Mutual Funds", "allocation": 25, "description": "Tax-saving equity funds for wealth creation", "funds": get_specific_fund_recommendations("Moderate", "ELSS")},
                        {"name": "Fixed Deposits", "allocation": 20, "description": "Stability anchor", "funds": get_specific_fund_recommendations("Moderate", "FD")},
                        {"name": "Medium Duration Debt Funds", "allocation": 15, "description": "Enhanced debt returns"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "SIP in Balanced Advantage, Hybrid MF + ELSS",
                    "products": [
                        {"name": "Balanced Advantage Fund SIP", "allocation": 45, "description": "Systematic dynamic allocation", "funds": get_specific_fund_recommendations("Moderate", "Balanced Advantage MF")},
                        {"name": "ELSS SIP", "allocation": 30, "description": "Tax-saving systematic investments", "funds": get_specific_fund_recommendations("Moderate", "ELSS")},
                        {"name": "Hybrid Fund SIP", "allocation": 25, "description": "Balanced debt-equity exposure"}
                    ]
                }
            },
            "7+ Years": {
                "lumpsum_yes": {
                    "primary": "Index / Large Cap MF + ELSS (Lumpsum + SIP)",
                    "products": [
                        {"name": "Index Funds", "allocation": 35, "description": "Low-cost market returns", "funds": get_specific_fund_recommendations("Moderate", "Index / Large Cap MF")},
                        {"name": "Large Cap Mutual Funds", "allocation": 30, "description": "Stable large company exposure"},
                        {"name": "ELSS", "allocation": 20, "description": "Tax-saving equity growth", "funds": get_specific_fund_recommendations("Moderate", "ELSS")},
                        {"name": "International Funds", "allocation": 10, "description": "Global diversification"},
                        {"name": "PPF/ELSS", "allocation": 5, "description": "Tax-efficient long-term savings"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "SIP in Index / Large Cap MF + ELSS",
                    "products": [
                        {"name": "Index Fund SIP", "allocation": 40, "description": "Systematic market investment", "funds": get_specific_fund_recommendations("Moderate", "Index / Large Cap MF")},
                        {"name": "Large Cap Fund SIP", "allocation": 30, "description": "Disciplined equity accumulation"},
                        {"name": "ELSS SIP", "allocation": 25, "description": "Tax-saving systematic plan", "funds": get_specific_fund_recommendations("Moderate", "ELSS")},
                        {"name": "PPF", "allocation": 5, "description": "Guaranteed long-term component"}
                    ]
                }
            }
        },
        "Aggressive": {
            "< 3 Years": {
                "lumpsum_yes": {
                    "primary": "FD (Emergency Lumpsum)",
                    "products": [
                        {"name": "Fixed Deposits", "allocation": 80, "description": "Capital preservation for short-term aggressive goals", "funds": get_specific_fund_recommendations("Aggressive", "FD")},
                        {"name": "Liquid Plus Funds", "allocation": 15, "description": "Enhanced liquidity returns"},
                        {"name": "Overnight Funds", "allocation": 5, "description": "Ultra-safe parking"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "FD (SIP)",
                    "products": [
                        {"name": "Monthly FD", "allocation": 85, "description": "Systematic fixed investments", "funds": get_specific_fund_recommendations("Aggressive", "FD")},
                        {"name": "Liquid Fund SIP", "allocation": 15, "description": "Regular liquid fund accumulation"}
                    ]
                }
            },
            "3-7 Years": {
                "lumpsum_yes": {
                    "primary": "Multi-cap / Flexi-cap MF + ELSS (Lumpsum + SIP)",
                    "products": [
                        {"name": "Flexi-cap Mutual Funds", "allocation": 40, "description": "Flexible market cap allocation for growth", "funds": get_specific_fund_recommendations("Aggressive", "Multi-cap / Flexi-cap MF")},
                        {"name": "Multi-cap Mutual Funds", "allocation": 30, "description": "Diversified equity exposure"},
                        {"name": "ELSS", "allocation": 20, "description": "Tax-saving aggressive growth", "funds": get_specific_fund_recommendations("Aggressive", "ELSS")},
                        {"name": "Mid & Small Cap Funds", "allocation": 10, "description": "Higher growth potential"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "SIP in Flexi-cap / Multi-cap MF + ELSS",
                    "products": [
                        {"name": "Flexi-cap Fund SIP", "allocation": 45, "description": "Systematic aggressive equity investing", "funds": get_specific_fund_recommendations("Aggressive", "Multi-cap / Flexi-cap MF")},
                        {"name": "Multi-cap Fund SIP", "allocation": 30, "description": "Diversified systematic equity"},
                        {"name": "ELSS SIP", "allocation": 25, "description": "Tax-efficient aggressive SIP", "funds": get_specific_fund_recommendations("Aggressive", "ELSS")}
                    ]
                }
            },
            "7+ Years": {
                "lumpsum_yes": {
                    "primary": "Equity MF + ELSS (Lumpsum + SIP)",
                    "products": [
                        {"name": "Large Cap Equity Funds", "allocation": 30, "description": "Stable foundation for long-term growth", "funds": get_specific_fund_recommendations("Aggressive", "Equity MF")},
                        {"name": "Mid Cap Equity Funds", "allocation": 25, "description": "Higher growth potential"},
                        {"name": "Small Cap Equity Funds", "allocation": 20, "description": "Maximum growth exposure"},
                        {"name": "ELSS", "allocation": 15, "description": "Tax-saving equity component", "funds": get_specific_fund_recommendations("Aggressive", "ELSS")},
                        {"name": "International Equity Funds", "allocation": 10, "description": "Global growth opportunities"}
                    ]
                },
                "lumpsum_no": {
                    "primary": "SIP in Equity MF + ELSS",
                    "products": [
                        {"name": "Large Cap Equity SIP", "allocation": 35, "description": "Systematic large cap accumulation", "funds": get_specific_fund_recommendations("Aggressive", "Equity MF")},
                        {"name": "Mid Cap Equity SIP", "allocation": 30, "description": "Growth-focused systematic investing"},
                        {"name": "ELSS SIP", "allocation": 20, "description": "Tax-saving equity SIP", "funds": get_specific_fund_recommendations("Aggressive", "ELSS")},
                        {"name": "Small Cap SIP", "allocation": 15, "description": "High-growth systematic investment"}
                    ]
                }
            }
        }
    }
    
    # Get specific recommendations
    lumpsum_key = "lumpsum_yes" if lumpsum_available else "lumpsum_no"
    recommendations = recommendations_matrix[risk_category][time_horizon][lumpsum_key]
    
    # Calculate suggested monthly SIP amount (10-15% of monthly income)
    suggested_sip = monthly_income * 0.125 if monthly_income > 0 else 5000
    
    # Calculate suggested lumpsum amount (if available)
    suggested_lumpsum = max(0, total_savings - emergency_fund_needed) * 0.7 if lumpsum_available else 0
    
    result = {
        "status": "success",
        "risk_category": risk_category,
        "time_horizon": time_horizon,
        "lumpsum_available": lumpsum_available,
        "emergency_fund_needed": emergency_fund_needed,
        "suggested_sip_amount": suggested_sip,
        "suggested_lumpsum_amount": suggested_lumpsum,
        "primary_strategy": recommendations["primary"],
        "recommended_products": recommendations["products"],
        "investment_rationale": get_investment_rationale(risk_category, time_horizon, lumpsum_available)
    }
    
    # Save to state
    state["comprehensive_recommendations"] = result
    
    return result


def determine_time_horizon(goals: str, age: int) -> str:
    """Determine investment time horizon based on goals and age"""
    goals_lower = goals.lower()
    
    # Short-term indicators
    if any(keyword in goals_lower for keyword in ["emergency", "travel", "wedding", "car", "1 year", "2 year", "short"]):
        return "< 3 Years"
    
    # Long-term indicators  
    if any(keyword in goals_lower for keyword in ["retirement", "child education", "property", "house", "long", "10 year", "15 year"]):
        return "7+ Years"
    
    # Medium-term by default or based on age
    if age > 55:
        return "3-7 Years"  # Pre-retirement typically has medium-term focus
    
    return "3-7 Years"  # Default medium-term


def get_investment_rationale(risk_category: str, time_horizon: str, lumpsum_available: bool) -> str:
    """Provide rationale for the investment recommendations"""
    
    rationale_base = {
        "Conservative": "focuses on capital preservation with minimal risk",
        "Moderate": "balances growth potential with reasonable safety",
        "Aggressive": "prioritizes maximum growth potential with higher risk tolerance"
    }
    
    time_rationale = {
        "< 3 Years": "short time horizon requires capital protection and liquidity",
        "3-7 Years": "medium time horizon allows for balanced growth with some stability",
        "7+ Years": "long time horizon enables equity-focused wealth creation"
    }
    
    lumpsum_rationale = {
        True: "lumpsum availability enables immediate market participation and SIP for rupee cost averaging",
        False: "systematic investment through SIPs provides disciplined wealth creation and rupee cost averaging"
    }
    
    return f"This {risk_category.lower()} strategy {rationale_base[risk_category]} while your {time_rationale[time_horizon]}. The {lumpsum_rationale[lumpsum_available]}."


def get_specific_fund_recommendations(risk_category: str, fund_type: str) -> List[Dict[str, Any]]:
    """
    Returns specific fund recommendations with historical returns based on risk category and fund type.
    
    Args:
        risk_category: Conservative, Moderate, or Aggressive
        fund_type: Type of fund (FD, Short-term Debt MF, etc.)
    
    Returns:
        List of specific fund recommendations with returns
    """
    
    # Specific fund recommendations with historical returns from market data
    fund_database = {
        "Conservative": {
            "FD": [
                {"name": "HDFC Fixed Deposit", "return": "7.00%", "description": "Secure fixed returns"},
                {"name": "SBI Fixed Deposit", "return": "7.00%", "description": "Government bank safety"},
                {"name": "ICICI Fixed Deposit", "return": "7.00%", "description": "Private bank reliability"}
            ],
            "Short-term Debt MF": [
                {"name": "HDFC Short Term Debt Fund", "return": "7.50%", "description": "Low duration risk, stable returns"},
                {"name": "ICICI Prudential Short Term Fund", "return": "8.23%", "description": "Better returns than FDs with moderate risk"}
            ],
            "Conservative Hybrid MF": [
                {"name": "HDFC Hybrid Debt Fund", "return": "7.00%", "description": "Debt-heavy hybrid for safety"},
                {"name": "Aditya Birla Balanced Advantage Fund", "return": "8.00%", "description": "Dynamic allocation with conservative bias"}
            ]
        },
        "Moderate": {
            "FD": [
                {"name": "HDFC Fixed Deposit", "return": "7.00%", "description": "Stable base component"},
                {"name": "SBI Fixed Deposit", "return": "7.00%", "description": "Government backing"},
                {"name": "ICICI Fixed Deposit", "return": "7.00%", "description": "Consistent performer"}
            ],
            "Arbitrage / Low Duration Debt MF": [
                {"name": "Nippon India Arbitrage Fund", "return": "6.50%", "description": "Equity taxation with debt-like risk"},
                {"name": "ICICI Prudential Arbitrage Fund", "return": "7.50%", "description": "Market neutral strategy"},
                {"name": "HDFC Low Duration Fund", "return": "7.00%", "description": "Minimal interest rate risk"}
            ],
            "Balanced Advantage MF": [
                {"name": "HDFC Balanced Advantage Fund", "return": "8.50%", "description": "Dynamic asset allocation leader"},
                {"name": "ICICI Prudential Balanced Advantage Fund", "return": "9.00%", "description": "Tactical allocation expertise"}
            ],
            "ELSS": [
                {"name": "Mirae Asset Tax Saver Fund", "return": "12.50%", "description": "Tax-saving equity with growth focus"},
                {"name": "Axis Long Term Equity Fund", "return": "13.00%", "description": "Consistent tax-saving performer"},
                {"name": "Aditya Birla Sun Life Tax Relief 96", "return": "13.50%", "description": "Long-term wealth creation with tax benefits"}
            ],
            "Index / Large Cap MF": [
                {"name": "Nippon India Large Cap Fund", "return": "10.00%", "description": "Large cap focused growth"},
                {"name": "HDFC Index Fund – Nifty 50 Plan", "return": "11.00%", "description": "Low-cost index tracking"},
                {"name": "SBI Bluechip Fund", "return": "12.00%", "description": "Quality large cap selection"}
            ]
        },
        "Aggressive": {
            "FD": [
                {"name": "HDFC Fixed Deposit", "return": "7.00%", "description": "Emergency funds only"},
                {"name": "SBI Fixed Deposit", "return": "7.00%", "description": "Liquidity component"},
                {"name": "ICICI Fixed Deposit", "return": "7.00%", "description": "Short-term parking"}
            ],
            "Multi-cap / Flexi-cap MF": [
                {"name": "Parag Parikh Flexi Cap Fund", "return": "12.50%", "description": "Global exposure with flexi-cap approach"},
                {"name": "Kotak Standard Multicap Fund", "return": "13.67%", "description": "Multi-cap diversification"},
                {"name": "Mirae Asset Emerging Bluechip Fund", "return": "14.23%", "description": "Mid-cap focused growth"}
            ],
            "Equity MF": [
                {"name": "Mirae Asset Large Cap Fund", "return": "12.25%", "description": "Quality large cap growth"},
                {"name": "Canara Robeco Equity Diversified Fund", "return": "13.50%", "description": "Diversified equity strategy"},
                {"name": "Axis Bluechip Fund", "return": "14.65%", "description": "Premium equity selection"}
            ],
            "ELSS": [
                {"name": "Mirae Asset Tax Saver Fund", "return": "12.50%", "description": "Growth-oriented tax saver"},
                {"name": "Axis Long Term Equity Fund", "return": "13.00%", "description": "Aggressive tax-saving approach"},
                {"name": "Aditya Birla Sun Life Tax Relief 96", "return": "13.50%", "description": "High-growth tax benefits"}
            ]
        }
    }
    
    return fund_database.get(risk_category, {}).get(fund_type, [])