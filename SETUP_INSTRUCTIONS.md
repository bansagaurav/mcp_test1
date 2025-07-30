# Quick Setup Instructions for MCP Sum Server

## Why This File?
This is a condensed version of the setup instructions for users who want to get started quickly without reading the full README.md documentation.

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Setup Steps

1. **Create Virtual Environment** (recommended):
   ```bash
   python3 -m venv mcp_env
   source mcp_env/bin/activate  # On Windows: mcp_env\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the Server**:
   ```bash
   python3 test_server.py
   ```

4. **Run the Server**:
   ```bash
   python3 mcp_sum_server.py
   ```

## What You'll See
- The server will start and show log messages
- It will wait for MCP protocol messages on stdin/stdout
- Use Ctrl+C to stop the server

## Files in This Project
- `mcp_sum_server.py` - Main MCP server with extensive comments
- `requirements.txt` - Python dependencies with explanations
- `README.md` - Comprehensive documentation
- `test_server.py` - Test script to verify functionality
- `SETUP_INSTRUCTIONS.md` - This quick setup guide

## Need Help?
Read the full `README.md` for detailed explanations of every component.