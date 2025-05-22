# Financial Risk Assessor Agent

A sophisticated AI agent that evaluates a user's financial risk profile and provides tailored investment recommendations using the Google Agent Development Kit (ADK).

## Overview

The Financial Risk Assessor guides users through a comprehensive financial assessment process:

1. **Collects user profile information** - Gathers demographic and financial data
2. **Analyzes investment portfolio** - Records and evaluates existing assets and investments
3. **Assesses risk tolerance** - Calculates numerical risk scores and risk categorization
4. **Provides tailored recommendations** - Suggests asset allocation and investment products

This agent demonstrates multiple ADK agent patterns working together:
- **Sequential agents** for step-by-step workflows
- **Parallel agents** for concurrent recommendation generation
- **LLM agents** for natural conversation and data collection
- **State management** for collecting and processing financial data
- **Azure GPT-4.1 integration** via LiteLLM for advanced reasoning

## Project Structure

```
13-financial-risk-assessor/
│
├── financial_risk_assessor/         # Main agent package
│   ├── __init__.py                  # Package initialization
│   ├── agent.py                     # Sequential Agent definition (root_agent)
│   │
│   └── subagents/                   # Sub-agents folder
│       ├── __init__.py              # Sub-agents initialization
│       │
│       ├── collect_user_profile/    # User profile collection agent
│       │   ├── __init__.py
│       │   ├── agent.py             # Sequential agent implementation
│       │   └── tools.py             # Tools for collecting user data
│       │
│       ├── collect_investment_data/ # Investment data collection agent
│       │   ├── __init__.py
│       │   ├── agent.py             # LLM agent implementation
│       │   └── tools.py             # Tools for collecting investment data
│       │
│       ├── analyze_risk_tolerance/  # Risk analysis agent
│       │   ├── __init__.py
│       │   ├── agent.py             # Risk analysis implementation
│       │   └── tools.py             # Tools for risk scoring and recommendations
│       │
│       └── generate_recommendations/  # Investment recommendation agent
│           ├── __init__.py
│           ├── agent.py             # Parallel agent with sub-agents
│           └── tools.py             # Tools for asset allocation and recommendations
│
└── README.md                        # This documentation
```

## Implementation Status

- **Completed**:
  - Root agent structure (Sequential)
  - User profile collection subagent (Sequential)
  - Investment data collection subagent (LLM Agent) with explicit confirmation
  - Risk tolerance analysis agent with portfolio assessment
  - Recommendation generation agent (Parallel) with specialized sub-agents
  - Tools for collecting and validating user data
  - Tools for iterative asset collection
  - Tools for risk scoring and investment recommendations
  - Tools for asset allocation and product recommendations
  - Comprehensive risk report generation
  - Integration with Azure GPT-4.1 via LiteLLM

- **Planned**:
  - Additional visualization capabilities
  - Portfolio optimization algorithms

## How It Works

1. **User Profile Collection**:
   - Collects age, income, expenses, savings, goals, and risk appetite
   - Validates data for completeness and performs basic sanity checks

2. **Investment Data Collection**:
   - Uses an LLM agent to iteratively collect multiple investment entries
   - For each investment, collects:
     - Asset type (stocks, bonds, real estate, etc.)
     - Asset details (amount, name, expected returns, etc.)
   - Continues collecting until the user has no more assets to add
   - Requires explicit confirmation before proceeding to risk analysis
   - Stores all investments in the session state

3. **Risk Assessment**:
   - Calculates risk score based on age, income stability, savings buffer, and stated risk appetite
   - Analyzes portfolio diversity and asset allocation
   - Identifies potential concentration risks
   - Assigns a risk category (Conservative, Moderate, or Aggressive)

4. **Recommendation Generation** (Parallel Processing):
   - **Asset Allocation Sub-agent**: 
     - Creates personalized allocation percentages across asset classes
     - Adjusts for age and risk profile
     - Provides detailed equity breakdowns
   - **Investment Products Sub-agent**: 
     - Recommends specific investment vehicles for each asset class
     - Tailors recommendations to risk category
     - Suggests tax-advantaged options
   - **Risk Report Sub-agent**:
     - Compiles comprehensive assessment summary
     - Provides age-specific guidance
     - Outlines clear next steps
     - Generates detailed portfolio analysis

## Getting Started

### Prerequisites

- Python 3.9+
- Google ADK installed (`pip install google-adk`)
- Azure OpenAI API key (set in `.env` file)

### Running the Agent

1. Navigate to the parent directory:
   ```bash
   cd /Users/admin/Documents/Projects/ai/google-adk
   ```

2. Start the interactive web UI:
   ```bash
   adk web
   ```

3. Select "financial_risk_assessor" from the dropdown menu in the web UI

4. Start a conversation with the agent by describing your financial situation

## Sample Interaction

```
User: I'd like to get a financial risk assessment.

Agent: Welcome to your financial risk assessment! I'll help you understand your financial risk profile and provide tailored investment recommendations.

To get started, I'll need to collect some basic information about your financial situation. This helps me provide accurate and personalized recommendations.

1. Could you tell me your age?
2. What is your annual income (in dollars)?
3. What are your typical monthly expenses (in dollars)?
4. How much do you have in total savings and investments (in dollars)?
5. What are your main financial goals? (e.g., retirement, home purchase, education)
6. How would you describe your risk appetite? (conservative, moderate, or aggressive)

Your information will be kept confidential and is only used for this risk assessment.

User: [Provides profile information]

Agent: Thank you for sharing your financial information. Now I'd like to collect details about your investments and assets. 
Let's start with the first one. What type of asset would you like to record first?

User: I have some stocks.

Agent: Great! Let's record your stock investments. 
Please provide the following details...

[Investment collection continues iteratively for each asset]

Agent: Based on your financial profile and investment portfolio, I've conducted a comprehensive risk analysis. Here's what I found:

[Provides detailed risk assessment and personalized investment recommendations]
```

## Example Prompts to Try

Here are some example prompts you can use to interact with the Financial Risk Assessor:

### Starting a New Assessment
```
I'd like to get a financial risk assessment for my retirement planning.
```

```
Can you help me understand my investment risk profile?
```

### During Profile Collection
```
I'm 42, earn $85,000 annually, spend about $4,000 monthly, and have $120,000 in savings. My main goal is saving for retirement in 20 years, and I consider myself moderately risk-tolerant.
```

```
My age is 35, I make $95,000 per year with monthly expenses of $3,500. I've saved $65,000 so far. I'm saving for a house down payment and college for my kids, and I'm somewhat conservative with risk.
```

### During Investment Collection
```
I have $50,000 in a S&P 500 index fund that I purchased 3 years ago. It's currently worth $62,000 with an average annual return of about 7%.
```

```
I own a rental property that I bought for $300,000 five years ago. Its current value is approximately $380,000, and it generates about $2,200 in monthly rental income.
```

```
I have $25,000 in a high-yield savings account earning 3.5% annually.
```

```
No, I don't have any more assets to add.
```

## Future Enhancements

- Database integration for persistent storage of user profiles
- Charts and visualizations for risk analysis
- Integration with real-time market data
- Support for international markets and currencies
- Portfolio optimization algorithms
- Tax-optimization suggestions
- Rebalancing recommendations for existing portfolios
- Monte Carlo simulations for retirement planning

## Additional Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Sequential Agents in ADK](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
- [LiteLLM Integration in ADK](https://google.github.io/adk-docs/tutorials/agent-team/#step-2-going-multi-model-with-litellm-optional)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)