"""
MCP Client for listing and reading resources and tools.

This script demonstrates how to connect to an MCP (Model Context Protocol) server
and interact with its resources and tools. It lists all available resources,
reads their content (expecting AgentCard JSON data), and lists available tools.

Usage:
    python mcp_client_list.py

Requirements:
    - fastmcp library
    - MCP server running at http://127.0.0.1:8080/mcp
"""

import asyncio
import json
from fastmcp import Client


async def main():
    """
    Main function to demonstrate MCP client capabilities.

    This function performs three main operations:
    1. Lists all available resources from the MCP server
    2. Reads and displays the content of each resource (AgentCards)
    3. Lists all available tools provided by the server

    The client connects to a local MCP server and uses the fastmcp library
    to communicate using the Model Context Protocol.
    """
    # Initialize the MCP client with the server endpoint
    client = Client("http://127.0.0.1:8080/mcp")

    # Use async context manager to ensure proper connection handling
    async with client:
        # ===== List Resources =====
        # Resources typically represent data objects like AgentCards, documents, etc.
        resources = await client.list_resources()
        print("Resources:")
        for r in resources:
            print(f" - {r.uri} ({r.name})")

        # ===== Retrieve and Display AgentCard Content =====
        # For each resource, read its content and display it as formatted JSON
        print("\nAgentCards:")
        for r in resources:
            # Read the resource content from the server
            content = await client.read_resource(r.uri)

            # Content is returned as a list of Content objects
            # Each Content object may have a 'text' attribute containing the data
            for c in content:
                if hasattr(c, "text") and c.text:
                    try:
                        # Attempt to parse the content as JSON (AgentCard format)
                        card = json.loads(c.text)
                        print(f"\n{r.uri}:")
                        # Pretty-print the JSON with 2-space indentation
                        print(json.dumps(card, indent=2))
                    except json.JSONDecodeError:
                        # If content is not valid JSON, display it as raw text
                        print(f"\n{r.uri}:")
                        print(c.text)

        # ===== List Available Tools =====
        # Tools represent callable functions/operations provided by the server
        tools = await client.list_tools()
        print("\nTools:")
        for t in tools:
            print(f"\n - {t.name}: {t.description}\n ")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

 