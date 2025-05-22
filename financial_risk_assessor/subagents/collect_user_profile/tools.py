"""
Tools for collecting and validating user profile information for financial risk assessment.
"""

from typing import Dict, List, Optional
from google.adk.tools.tool_context import ToolContext


def collect_user_info(
    age: int,
    annual_income: float,
    monthly_expenses: float, 
    total_savings: float,
    financial_goals: str,
    risk_appetite: str,
    tool_context: ToolContext,
) -> Dict:
    """
    Collects user's demographic and financial background information.
    
    Args:
        age: User's age in years
        annual_income: Annual income in dollars
        monthly_expenses: Monthly expenses in dollars
        total_savings: Total savings and investments in dollars
        financial_goals: Description of financial goals (e.g., retirement, house purchase)
        risk_appetite: Self-described risk tolerance (e.g., conservative, moderate, aggressive)
        tool_context: Tool context with access to state
    
    Returns:
        Dictionary with collected user information and success message
    """
    # Store user profile data in state
    tool_context.state["user_profile"] = {
        "age": age,
        "annual_income": annual_income,
        "monthly_expenses": monthly_expenses,
        "total_savings": total_savings,
        "financial_goals": financial_goals,
        "risk_appetite": risk_appetite,
    }
    
    return {
        "status": "success",
        "message": "User profile information collected successfully.",
        "profile_data": tool_context.state["user_profile"],
    }


def validate_user_data(tool_context: ToolContext) -> Dict:
    """
    Validates collected user data for completeness and basic sanity checks.
    
    Args:
        tool_context: Tool context with access to state
    
    Returns:
        Dictionary with validation results, including status and any missing or problematic fields
    """
    user_profile = tool_context.state.get("user_profile", {})
    missing_fields = []
    issues = []
    
    # Check for missing required fields
    required_fields = ["age", "annual_income", "monthly_expenses", "total_savings", 
                      "financial_goals", "risk_appetite"]
                      
    for field in required_fields:
        if field not in user_profile or user_profile[field] is None:
            missing_fields.append(field)
    
    # Validate data integrity
    if "age" in user_profile and user_profile["age"]:
        if user_profile["age"] < 18 or user_profile["age"] > 120:
            issues.append("Age must be between 18 and 120 years")
    
    if "annual_income" in user_profile and user_profile["annual_income"]:
        if user_profile["annual_income"] < 0:
            issues.append("Annual income cannot be negative")
    
    if "monthly_expenses" in user_profile and user_profile["monthly_expenses"]:
        if user_profile["monthly_expenses"] < 0:
            issues.append("Monthly expenses cannot be negative")
        if "annual_income" in user_profile and user_profile["annual_income"]:
            if user_profile["monthly_expenses"] * 12 > user_profile["annual_income"] * 1.5:
                issues.append("Monthly expenses seem unusually high compared to income")
    
    if "total_savings" in user_profile and user_profile["total_savings"] is not None:
        if user_profile["total_savings"] < 0:
            issues.append("Total savings cannot be negative")
    
    # Store validation results in state
    validation_result = {
        "is_valid": len(missing_fields) == 0 and len(issues) == 0,
        "missing_fields": missing_fields,
        "issues": issues,
    }
    
    tool_context.state["validation_result"] = validation_result
    
    return {
        "status": "success" if validation_result["is_valid"] else "incomplete",
        "message": "User data is complete and valid" if validation_result["is_valid"] 
                  else "User data has issues that need to be addressed",
        "missing_fields": missing_fields,
        "issues": issues,
        "validation_result": validation_result,
    }