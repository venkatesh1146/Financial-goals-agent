#!/usr/bin/env python3
"""
Script to run the Financial Risk Assessor API server.
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("API_PORT", "8000"))
    
    # Start the FastAPI server
    print(f"Starting Financial Risk Assessor API on port {port}...")
    print(f"API documentation will be available at http://localhost:{port}/docs")
    print("✨ New: Comprehensive investment recommendations based on risk profile, time horizon, and lumpsum availability")
    print("🌐 CORS enabled for Next.js development (ports 3000, 3001)")
    
    uvicorn.run(
        "financial_risk_assessor.api:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )