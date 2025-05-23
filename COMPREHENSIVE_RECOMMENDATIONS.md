# Comprehensive Investment Recommendations

## Overview

The Financial Risk Assessor now includes a comprehensive investment recommendation system based on a decision matrix that considers three key factors:

1. **Risk Profile** (Conservative, Moderate, Aggressive)
2. **Time Horizon** (< 3 Years, 3-7 Years, 7+ Years)
3. **Lumpsum Availability** (Yes/No)

## Decision Matrix Logic

The system automatically determines:

### Time Horizon
- **< 3 Years**: Keywords like "emergency", "travel", "wedding", "car", "short-term"
- **3-7 Years**: Default for most goals, pre-retirement age (55+)
- **7+ Years**: Keywords like "retirement", "child education", "property", "long-term"

### Lumpsum Availability
- **Available**: Total savings > (6 months of expenses) 
- **Not Available**: Insufficient savings after emergency fund

### Risk Profile
- Determined by the existing risk assessment agent based on user profile and preferences

## Investment Recommendations by Category

### Conservative Investors

#### < 3 Years
- **With Lumpsum**: FD (Lumpsum) - Focus on Fixed Deposits with Liquid Funds
- **Without Lumpsum**: FD (SIP) - Monthly FD investments with systematic approach

#### 3-7 Years  
- **With Lumpsum**: FD + Short-term Debt MF (Lumpsum + SIP)
- **Without Lumpsum**: SIP in Short-term Debt / Conservative Hybrid MF

#### 7+ Years
- **With Lumpsum**: FD + Conservative Hybrid MF (Lumpsum + SIP) + ELSS
- **Without Lumpsum**: SIP in Conservative Hybrid MF + ELSS + PPF

### Moderate Investors

#### < 3 Years
- **With Lumpsum**: FD + Arbitrage / Low Duration Debt MF
- **Without Lumpsum**: FD only, avoid equity SIP for short-term

#### 3-7 Years
- **With Lumpsum**: Balanced Advantage MF + ELSS + FD (Lumpsum + SIP)
- **Without Lumpsum**: SIP in Balanced Advantage + Hybrid MF + ELSS

#### 7+ Years
- **With Lumpsum**: Index / Large Cap MF + ELSS (Lumpsum + SIP)
- **Without Lumpsum**: SIP in Index / Large Cap MF + ELSS

### Aggressive Investors

#### < 3 Years
- **With Lumpsum**: FD (Emergency Lumpsum) - Even aggressive investors need capital protection for short-term
- **Without Lumpsum**: FD (SIP) - Systematic fixed investments

#### 3-7 Years
- **With Lumpsum**: Multi-cap / Flexi-cap MF + ELSS (Lumpsum + SIP)
- **Without Lumpsum**: SIP in Flexi-cap / Multi-cap MF + ELSS

#### 7+ Years
- **With Lumpsum**: Equity MF + ELSS (Lumpsum + SIP) - Maximum equity exposure
- **Without Lumpsum**: SIP in Equity MF + ELSS

## Key Features

### Automatic Calculations
- **SIP Amount**: 12.5% of monthly income (default: ₹5,000)
- **Lumpsum Amount**: 70% of (Total Savings - Emergency Fund)
- **Emergency Fund**: 6 months of expenses

### Specific Fund Recommendations
Each recommendation now includes specific mutual funds with historical returns:
- **HDFC Balanced Advantage Fund** (8.50% returns) for moderate balanced strategies
- **Mirae Asset Tax Saver Fund** (12.50% returns) for ELSS recommendations
- **Parag Parikh Flexi Cap Fund** (12.50% returns) for aggressive growth
- **ICICI Prudential Short Term Fund** (8.23% returns) for conservative debt strategies

### Product Allocations
Each recommendation includes specific allocation percentages and descriptions for:
- Fixed Deposits (HDFC, SBI, ICICI - 7% returns)
- Mutual Funds (various types with historical performance)
- ELSS (Tax-saving funds with 12.5-13.5% returns)
- PPF/EPF
- Liquid Funds
- Alternative investments

### Enhanced API Response
The API now returns:
```json
{
  "comprehensive_recommendations": {
    "risk_category": "Moderate",
    "time_horizon": "7+ Years",
    "lumpsum_available": true,
    "suggested_sip_amount": 75000,
    "suggested_lumpsum_amount": 140000,
    "primary_strategy": "Index / Large Cap MF + ELSS (Lumpsum + SIP)",
    "recommended_products": [
      {
        "name": "Index Funds",
        "allocation": 35,
        "description": "Low-cost market returns",
        "funds": [
          {
            "name": "HDFC Index Fund – Nifty 50 Plan",
            "return": "11.00%",
            "description": "Low-cost index tracking"
          }
        ]
      }
    ],
    "investment_rationale": "..."
  }
}
```

## Testing

Run the test script to see different scenarios:

```bash
python test_comprehensive_recommendations.py
```

This will test 4 different user profiles showcasing various combinations of the decision matrix.

## API Usage

The existing API endpoint `/analyze` now includes comprehensive recommendations automatically. No changes needed to existing API calls.

## Implementation Details

### Files Modified
- `financial_risk_assessor/subagents/generate_recommendations/tools.py` - Added comprehensive recommendation logic
- `financial_risk_assessor/subagents/generate_recommendations/agent.py` - Updated to use new recommendation tool
- `financial_risk_assessor/api.py` - Enhanced API response
- `run_api.py` - Updated startup message

### New Functions
- `get_comprehensive_investment_recommendations()` - Main decision matrix implementation
- `determine_time_horizon()` - Time horizon detection from goals and age
- `get_investment_rationale()` - Provides reasoning for recommendations

The system maintains backward compatibility while providing much more detailed and contextually appropriate investment recommendations. 