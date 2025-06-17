[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/sam06002-mcp-test1-badge.png)](https://mseep.ai/app/sam06002-mcp-test1)

# MCP Outlet Management Demo

This is a prototype demonstrating the "change outlet name" workflow using the Model Context Protocol (MCP). The demo includes a mock backend, MCP server, and client script.

## Project Structure

```
mcp-outlet-demo/
├── README.md
├── requirements.txt
├── .gitignore
├── backend/              # Mock backend server (Flask)
│   ├── __init__.py
│   ├── app.py
│   └── mock_data.py
├── mcp_server/          # MCP server implementation (FastAPI)
│   ├── __init__.py
│   └── server.py
└── client/              # Demo client script
    └── client.py
```

## Features

- **Backend (Flask)**: Mock API server that handles email verification and outlet name updates
- **MCP Server (FastAPI)**: Implements the Model Context Protocol for tool invocation
- **Client**: Demonstrates the complete workflow of verifying an email and updating an outlet name

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-outlet-demo
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Demo

1. Start the backend server (in a new terminal):
   ```bash
   cd backend
   python -m flask run --port 5001
   ```

2. Start the MCP server (in a new terminal):
   ```bash
   cd mcp_server
   python -m server
   ```

3. Run the client script (in a new terminal):
   ```bash
   cd client
   python -m client
   ```

## API Endpoints

### Backend API (Flask)
- `POST /verify_email` - Verify an email and return outlet information
- `POST /update_outlet_name` - Update the name of an outlet

### MCP Server (FastAPI)
- `POST /verify_email` - MCP-compatible email verification
- `POST /update_outlet_name` - MCP-compatible outlet name update
- `GET /health` - Health check endpoint

## Environment Variables

- `BACKEND_URL`: URL of the backend server (default: `http://localhost:5001`)

## Testing

You can test the API endpoints directly using `curl`:

```bash
# Verify email
curl -X POST http://localhost:8001/verify_email -H "Content-Type: application/json" -d '{"email":"demo@example.com"}'

# Update outlet name
curl -X POST http://localhost:8001/update_outlet_name -H "Content-Type: application/json" -d '{"email":"demo@example.com","new_name":"New Outlet Name"}'
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Setup

1. **Clone the repository** (if not already done)

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Demo

### 1. Start the Backend Server

In a new terminal window:

```bash
cd backend
python -m flask run --port 5000
```

The backend server will start on `http://localhost:5000`.

### 2. Start the MCP Server

In a new terminal window:

```bash
cd mcp_server
python -m server
```

The MCP server will start on `http://localhost:8000`.

### 3. Run the Client Script

In a new terminal window:

```bash
cd client
python client.py
```

## Expected Output

When you run the client script, you should see output similar to:

```
Starting MCP workflow for email: demo@example.com
--------------------------------------------------
1. Verifying email...
Verification result: {
  "status": "verified",
  "outlet": {
    "outlet_id": 1,
    "name": "Demo Outlet"
  }
}

2. Updating outlet name...
Update result: {
  "status": "success",
  "outlet": {
    "outlet_id": 1,
    "name": "Updated Demo Outlet"
  }
}

✅ Successfully completed the workflow!
Outlet name updated to: Updated Demo Outlet
```

## API Endpoints

### Backend API

- `POST /verify_email`
  - Request body: `{ "email": "string" }`
  - Success response: `{ "status": "verified", "outlet": { "outlet_id": number, "name": "string" } }`
  - Error response: `{ "error": "string" }` with 404 status

- `POST /update_outlet_name`
  - Request body: `{ "email": "string", "new_name": "string" }`
  - Success response: `{ "status": "success", "outlet": { "outlet_id": number, "name": "string" } }`
  - Error response: `{ "error": "string" }` with 400/404 status

### MCP Tools

- `verify_email(email: str)`: Verifies if an email exists and returns outlet information
- `update_outlet_name(email: str, new_name: str)`: Updates the name of an outlet

## License

This project is for demonstration purposes only.
