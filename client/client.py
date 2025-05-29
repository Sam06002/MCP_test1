import asyncio
import httpx
import json
from typing import Dict, Any

async def invoke_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoke a tool on the MCP server.
    
    Args:
        tool_name: Name of the tool to invoke (without the /mcp/invoke/ prefix)
        params: Parameters to pass to the tool
        
    Returns:
        The JSON response from the server
    """
    async with httpx.AsyncClient() as client:
        try:
            # For our simplified MCP server, we call the endpoints directly
            if tool_name == "verify_email":
                response = await client.post(
                    "http://localhost:8001/verify_email",
                    json=params,
                    timeout=10.0
                )
            elif tool_name == "update_outlet_name":
                response = await client.post(
                    "http://localhost:8001/update_outlet_name",
                    json=params,
                    timeout=10.0
                )
            else:
                return {"error": f"Unknown tool: {tool_name}"}
                
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            return {"error": f"Error invoking tool: {str(e)}"}

async def main():
    # Email to test with
    email = "demo@example.com"
    new_name = "Updated Demo Outlet"
    
    print(f"Starting MCP workflow for email: {email}")
    print("-" * 50)
    
    try:
        # Step 1: Verify email
        print("1. Verifying email...")
        verify_result = await invoke_tool("verify_email", {"email": email})
        print(f"Verification result: {json.dumps(verify_result, indent=2)}")
        
        if verify_result.get('error') or not verify_result.get('outlet'):
            print(f"Error verifying email: {verify_result.get('error', 'Unknown error')}")
            return
        
        # Step 2: Update outlet name
        print("\n2. Updating outlet name...")
        update_result = await invoke_tool("update_outlet_name", {
            "email": email, 
            "new_name": new_name
        })
        print(f"Update result: {json.dumps(update_result, indent=2)}")
        
        if update_result.get('error'):
            print(f"Error updating outlet name: {update_result.get('error')}")
        else:
            print("\n✅ Successfully completed the workflow!")
            print(f"Outlet name updated to: {update_result.get('outlet', {}).get('name')}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
