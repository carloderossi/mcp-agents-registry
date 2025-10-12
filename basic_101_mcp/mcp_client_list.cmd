@echo off

@title MCP Client - List Tools and Resources

REM Change to project directory
cd /d C:\Carlo\projects\mcp

REM Run the client Agent inside the uv-managed .venv
cd /d C:\Carlo\projects\mcp\basic_101_mcp
uv run python mcp_client_list.py


pause