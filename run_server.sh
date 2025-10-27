#!/bin/bash
# run_server.sh - Convenience script to start the MCP server
#
# WHY THIS FILE EXISTS:
# Instead of having to remember and type multiple commands every time,
# this script does everything needed to start the server in one command.
#
# WHAT IT DOES:
# 1. Activates the Python virtual environment (venv)
# 2. Runs the MCP server with the correct Python interpreter
#
# HOW TO USE:
# Make it executable: chmod +x run_server.sh
# Then run: ./run_server.sh
#
# ALTERNATIVE (without this script):
# source venv/bin/activate
# python3 mcp_server.py

echo "🚀 Starting Simple Addition MCP Server..."
echo "📁 Activating virtual environment..."

# Activate virtual environment (where our packages are installed)
source venv/bin/activate

echo "🧮 Starting the addition server..."
echo "💡 Connect an MCP client (like Claude Desktop) to use it!"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Run the MCP server
python3 mcp_server.py