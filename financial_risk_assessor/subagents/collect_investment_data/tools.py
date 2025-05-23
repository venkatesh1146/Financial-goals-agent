"""
Tools for collecting investment and asset data for financial risk assessment.
"""

from typing import Dict, List, Optional
from google.adk.tools.tool_context import ToolContext


ASSET_TYPES = [
    "Equities (Stocks)", 
    "Fixed Income (Bonds)", 
    "Real Estate", 
    "Cash & Equivalents", 
    "Gold & Precious Metals",
    "Alternative Investments", 
    "Cryptocurrencies", 
    "Mutual Funds",
    "ETFs",
    "Retirement Accounts"
]


def record_asset_type(
    asset_type: str,
    tool_context: ToolContext,
) -> Dict:
    """
    Records the type of asset being added to the portfolio.
    
    Args:
        asset_type: The type of asset (e.g., equity, debt, real estate, gold, etc.)
        tool_context: Tool context with access to state
    
    Returns:
        Dictionary with the selected asset type and available types
    """
    # Initialize the investments list in state if it doesn't exist
    if "investments" not in tool_context.state:
        tool_context.state["investments"] = []
    
    # Initialize the current investment entry
    tool_context.state["current_investment"] = {
        "asset_type": asset_type,
        "details": {}
    }
    
    return {
        "status": "success",
        "message": f"Asset type '{asset_type}' recorded successfully.",
        "available_types": ASSET_TYPES,
        "selected_type": asset_type,
    }


def record_asset_details(
    amount: float,
    name: str,
    expected_returns: Optional[float] = None,
    current_value: Optional[float] = None,
    purchase_date: Optional[str] = None,
    tenure: Optional[str] = None,
    risk_category: Optional[str] = None,
    additional_notes: Optional[str] = None,
    tool_context: ToolContext = None,
) -> Dict:
    """
    Records detailed information about an asset or investment.
    
    Args:
        amount: Initial investment amount in dollars
        name: Name or description of the asset/investment
        expected_returns: Expected annual returns as a percentage (optional)
        current_value: Current value of the asset in dollars (optional)
        purchase_date: When the asset was acquired (optional)
        tenure: How long the asset has been held or investment duration (optional)
        risk_category: User's assessment of the asset's risk (optional)
        additional_notes: Any additional information about this asset (optional)
        tool_context: Tool context with access to state
    
    Returns:
        Dictionary with the recorded asset details
    """
    if "current_investment" not in tool_context.state:
        return {
            "status": "error",
            "message": "No asset type has been selected. Please record an asset type first."
        }
    
    current_investment = tool_context.state["current_investment"]
    
    # Record details
    current_investment["details"] = {
        "amount": amount,
        "name": name,
        "expected_returns": expected_returns,
        "current_value": current_value if current_value is not None else amount,
        "purchase_date": purchase_date,
        "tenure": tenure,
        "risk_category": risk_category,
        "additional_notes": additional_notes,
    }
    
    # Add the completed investment to the investments list
    if "investments" not in tool_context.state:
        tool_context.state["investments"] = []
    
    # Store asset_type value before appending to investments to avoid KeyError
    asset_type = current_investment.get('asset_type', 'Unspecified')
    tool_context.state["investments"].append(current_investment)
    
    # Clear the current investment data so a new one can be started
    tool_context.state["current_investment"] = {}
    
    return {
        "status": "success",
        "message": f"Details for {name} ({asset_type}) recorded successfully.",
        "details": current_investment,
    }


def has_more_assets(has_more: bool, tool_context: ToolContext) -> Dict:
    """
    Records whether the user has more assets to add and controls the loop termination.
    
    Args:
        has_more: Boolean indicating if user has more assets to record
        tool_context: Tool context with access to state
    
    Returns:
        Dictionary with status and control information for the loop agent
    """
    tool_context.state["has_more_assets"] = has_more
    
    # Only mark investment collection as complete when:
    # 1. User explicitly confirms they have no more assets to add (has_more = False)
    # 2. At least one investment has been recorded
    assets_count = len(tool_context.state.get("investments", []))
    
    # Reset the investment_collection_complete flag to false by default
    tool_context.state["investment_collection_complete"] = False
    
    # Only set to true if user confirms completion AND we have at least one investment
    if not has_more and assets_count > 0:
        tool_context.state["investment_collection_complete"] = True
        tool_context.state["investment_collection_confirmed"] = True
    
    return {
        "status": "success",
        "message": "More assets status recorded.",
        "has_more_assets": has_more,
        "should_continue": has_more,
        "assets_recorded_count": assets_count,
        "collection_complete": not has_more and assets_count > 0,
        "collection_confirmed": not has_more and assets_count > 0
    }


def confirm_investment_completion(
    confirmed: bool,
    tool_context: ToolContext,
) -> Dict:
    """
    Explicitly confirms with the user that they are ready to proceed with risk analysis
    after completing investment data collection.
    
    Args:
        confirmed: Boolean indicating explicit user confirmation to proceed
        tool_context: Tool context with access to state
    
    Returns:
        Dictionary with confirmation status
    """
    assets_count = len(tool_context.state.get("investments", []))
    
    if confirmed and assets_count > 0:
        # User has explicitly confirmed they want to proceed with risk analysis
        tool_context.state["investment_collection_complete"] = True
        tool_context.state["investment_collection_confirmed"] = True
        
        return {
            "status": "success",
            "message": "Investment collection completed and confirmed.",
            "ready_for_risk_analysis": True,
            "investment_count": assets_count
        }
    elif confirmed and assets_count == 0:
        # User confirmed but no investments recorded yet
        return {
            "status": "warning",
            "message": "No investments have been recorded yet. Please add at least one investment before proceeding.",
            "ready_for_risk_analysis": False,
            "investment_count": 0
        }
    else:
        # User is not ready to proceed
        tool_context.state["investment_collection_complete"] = False
        tool_context.state["investment_collection_confirmed"] = False
        
        return {
            "status": "info",
            "message": "Let's continue collecting investment data.",
            "ready_for_risk_analysis": False,
            "investment_count": assets_count
        }