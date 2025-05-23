#!/usr/bin/env python3
"""
Test script for comprehensive investment recommendations

This script demonstrates the new decision matrix-based recommendation system
that considers risk profile, time horizon, and lumpsum availability.
"""

import requests
import json
from typing import Dict, Any

def test_recommendation_scenarios():
    """Test different user scenarios to showcase the decision matrix"""
    
    base_url = "http://localhost:8000"
    
    # Test scenarios covering different matrix combinations
    test_scenarios = [
        {
            "name": "Young Conservative with Lumpsum - Long term goals",
            "profile": {
                "age": 25,
                "income": 600000,  # 6 LPA
                "expenses": 25000,
                "savings": 300000,  # 3 Lakhs savings
                "goals": "retirement planning and long-term wealth creation",
                "risk_appetite": "conservative",
                "investments": [
                    {"type": "FD", "amount": 100000, "name": "Fixed Deposit"},
                    {"type": "savings", "amount": 200000, "name": "Savings Account"}
                ]
            }
        },
        {
            "name": "Middle-aged Moderate - Short term wedding goal",
            "profile": {
                "age": 35,
                "income": 1200000,  # 12 LPA
                "expenses": 60000,
                "savings": 500000,  # 5 Lakhs savings
                "goals": "wedding in 2 years and emergency fund",
                "risk_appetite": "moderate",
                "investments": [
                    {"type": "mutual_fund", "amount": 200000, "name": "Balanced Fund"},
                    {"type": "stocks", "amount": 150000, "name": "Equity Portfolio"},
                    {"type": "savings", "amount": 150000, "name": "Emergency Fund"}
                ]
            }
        },
        {
            "name": "Aggressive Investor - No Lumpsum available",
            "profile": {
                "age": 28,
                "income": 800000,  # 8 LPA
                "expenses": 45000,
                "savings": 200000,  # Only 2 Lakhs savings (less than 6 months expenses)
                "goals": "aggressive wealth creation for retirement",
                "risk_appetite": "aggressive",
                "investments": [
                    {"type": "ELSS", "amount": 100000, "name": "Tax Saving Fund"},
                    {"type": "savings", "amount": 100000, "name": "Emergency Fund"}
                ]
            }
        },
        {
            "name": "Pre-retirement Conservative - Medium term goals",
            "profile": {
                "age": 55,
                "income": 1500000,  # 15 LPA
                "expenses": 80000,
                "savings": 2000000,  # 20 Lakhs savings
                "goals": "retirement preparation and child education in 5 years",
                "risk_appetite": "conservative",
                "investments": [
                    {"type": "PPF", "amount": 500000, "name": "Public Provident Fund"},
                    {"type": "FD", "amount": 800000, "name": "Fixed Deposits"},
                    {"type": "mutual_fund", "amount": 400000, "name": "Hybrid Funds"},
                    {"type": "savings", "amount": 300000, "name": "Liquid Savings"}
                ]
            }
        }
    ]
    
    print("🧪 Testing Comprehensive Investment Recommendation System")
    print("=" * 60)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📊 Scenario {i}: {scenario['name']}")
        print("-" * 50)
        
        try:
            # Make API call
            response = requests.post(f"{base_url}/analyze", json=scenario["profile"])
            
            if response.status_code == 200:
                result = response.json()
                display_recommendations(result, scenario["name"])
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the API server is running on port 8000")
            print("Run: python run_api.py")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def display_recommendations(result: Dict[str, Any], scenario_name: str):
    """Display the recommendation results in a formatted way"""
    
    # Risk Assessment
    risk_assessment = result.get("risk_assessment", {})
    print(f"🎯 Risk Profile: {risk_assessment.get('risk_category', 'Unknown')} "
          f"(Score: {risk_assessment.get('risk_score', 'N/A')}/10)")
    
    # Comprehensive Recommendations
    comp_rec = result.get("comprehensive_recommendations", {})
    if comp_rec:
        print(f"⏰ Time Horizon: {comp_rec.get('time_horizon', 'Unknown')}")
        print(f"💰 Lumpsum Available: {'Yes' if comp_rec.get('lumpsum_available') else 'No'}")
        print(f"🎯 Primary Strategy: {comp_rec.get('primary_strategy', 'N/A')}")
        
        # Investment amounts
        sip_amount = comp_rec.get("suggested_sip_amount", 0)
        lumpsum_amount = comp_rec.get("suggested_lumpsum_amount", 0)
        
        if sip_amount > 0:
            print(f"📈 Suggested SIP: ₹{sip_amount:,.0f} per month")
        if lumpsum_amount > 0:
            print(f"💼 Suggested Lumpsum: ₹{lumpsum_amount:,.0f}")
        
        # Product recommendations
        products = comp_rec.get("recommended_products", [])
        if products:
            print("\n🏆 Recommended Products:")
            for product in products:
                print(f"  • {product['name']} ({product['allocation']}%): {product['description']}")
                
                # Show specific fund recommendations if available
                funds = product.get("funds", [])
                if funds:
                    print(f"    📈 Specific Fund Options:")
                    for fund in funds[:2]:  # Show top 2 funds
                        return_info = f" ({fund['return']})" if 'return' in fund else ""
                        print(f"      - {fund['name']}{return_info}: {fund['description']}")
        
        # Rationale
        rationale = comp_rec.get("investment_rationale", "")
        if rationale:
            print(f"\n💡 Strategy Rationale: {rationale}")
    
    # Next Steps
    next_steps = result.get("next_steps", [])
    if next_steps:
        print(f"\n📋 Next Steps:")
        for step in next_steps[:3]:  # Show first 3 steps
            print(f"  ✓ {step}")

if __name__ == "__main__":
    test_recommendation_scenarios() 