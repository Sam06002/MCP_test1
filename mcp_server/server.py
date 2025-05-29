import os
import json
import uvicorn
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Get backend URL from environment or use default
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5001")

# Create FastAPI app
app = FastAPI(title="MCP Outlet Management API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Outlet(BaseModel):
    outlet_id: int
    name: str

class VerifyEmailResponse(BaseModel):
    status: str
    outlet: Optional[Outlet] = None
    error: Optional[str] = None

class UpdateOutletNameResponse(BaseModel):
    status: str
    outlet: Optional[Outlet] = None
    error: Optional[str] = None

# API endpoints
class EmailRequest(BaseModel):
    email: str

@app.post("/verify_email", response_model=VerifyEmailResponse)
async def verify_email(request: EmailRequest) -> Dict[str, Any]:
    """
    Verify if an email exists in the system and return the associated outlet information.
    """
    email = request.email
    print(f"Verifying email: {email}")
    try:
        response = requests.post(
            f"{BACKEND_URL}/verify_email",
            json={"email": email},
            headers={"Content-Type": "application/json"}
        )
        print(f"Backend response status: {response.status_code}")
        print(f"Backend response content: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Failed to verify email: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Invalid JSON response from backend: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

class UpdateOutletNameRequest(BaseModel):
    email: str
    new_name: str

@app.post("/update_outlet_name", response_model=UpdateOutletNameResponse)
async def update_outlet_name(request: UpdateOutletNameRequest) -> Dict[str, Any]:
    """
    Update the name of an outlet associated with the given email.
    """
    email = request.email
    new_name = request.new_name
    print(f"Updating outlet name for {email} to {new_name}")
    try:
        response = requests.post(
            f"{BACKEND_URL}/update_outlet_name",
            json={"email": email, "new_name": new_name}
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update outlet name: {str(e)}")

# MCP-compatible endpoints
@app.post("/mcp/invoke/{tool_name}")
async def invoke_tool(tool_name: str, params: Dict[str, Any]):
    """
    MCP-compatible endpoint for tool invocation.
    """
    if tool_name == "verify_email":
        email = params.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        return await verify_email(email)
    
    elif tool_name == "update_outlet_name":
        email = params.get("email")
        new_name = params.get("new_name")
        if not email or not new_name:
            raise HTTPException(status_code=400, detail="Email and new_name are required")
        return await update_outlet_name(email, new_name)
    
    raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    # Start the server on port 8001
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
