"""
Mini MCP Client - Dynamic AgentCard Registration Demo

This script demonstrates the full lifecycle of AgentCard management via MCP:
- Listing existing agent cards and resources
- Registering a new agent dynamically
- Deregistering an agent
- Verifying changes after each operation

The script showcases how to use MCP tools to manage agent resources at runtime,
allowing dynamic addition and removal of agents without server restart.
This is used as an Eval for this small demo.

Usage:
    python mini_mcp_client.py

Requirements:
    - fastmcp library
    - MCP server running at http://127.0.0.1:8080/mcp with agent management tools
"""

import asyncio
import json
from fastmcp import Client


async def list_agent_cards(client):
    """
    List and display all available AgentCard resources from the MCP server.

    This function retrieves all resources (AgentCards) from the server and prints
    them in two formats:
    1. A summary list showing URI and name
    2. Full detailed content formatted as JSON

    Args:
        client: An active fastmcp.Client instance connected to the MCP server

    The function handles both JSON-formatted content (typical for AgentCards)
    and plain text content gracefully.
    """
    # Fetch all available resources from the server
    resources = await client.list_resources()
    print("Resources:")
    for r in resources:
        print(f" - {r.uri} ({r.name})")

    # Retrieve and display the full content of each resource
    print("\nAgentCards:")
    for r in resources:
        # Read the resource content by URI
        content = await client.read_resource(r.uri)

        # Content is returned as a list of Content objects
        # Each may have a 'text' attribute containing the actual data
        for c in content:
            if hasattr(c, "text") and c.text:
                try:
                    # Parse and pretty-print JSON content (standard AgentCard format)
                    card = json.loads(c.text)
                    print(f"\n{r.uri}:")
                    print(json.dumps(card, indent=2))
                except json.JSONDecodeError:
                    # Fallback to raw text if content is not valid JSON
                    print(f"\n{r.uri}:")
                    print(c.text)

async def main():
    """
    Main function demonstrating the complete AgentCard lifecycle.

    This function performs the following workflow:
    1. Lists initial agent cards and available tools
    2. Registers a new "PlannerAgent" dynamically
    3. Verifies the agent was added by listing cards again
    4. Deregisters the PlannerAgent
    5. Verifies the agent was removed by listing cards a final time

    This demonstrates how MCP servers can dynamically manage agent resources
    at runtime through tool calls, without requiring server restart.
    """
    # Initialize the MCP client with the server endpoint
    client = Client("http://127.0.0.1:8080/mcp")

    # Use async context manager for proper connection lifecycle management
    async with client:
        # ===== Initial State: List Existing AgentCards =====
        await list_agent_cards(client)

        # ===== List Available Tools =====
        # Display all tools provided by the server (including agent management tools)
        tools = await client.list_tools()
        print("\nTools:")
        for t in tools:
            print(f"\n - {t.name}: {t.description}\n ")

        # ===== Register a New AgentCard =====
        # Define a new agent with its capabilities and skills
        new_card = {
            "name": "PlannerAgent",
            "description": "Uses Ollama to create structured plans",
            "url": "http://localhost:9002/",
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "skills": [
                {
                    "id": "planning",
                    "name": "Planning",
                    "description": "Turn research into a step-by-step plan",
                    "tags": ["planning", "strategy"],
                    "examples": ["Make an experiment plan", "Outline next steps"]
                }
            ],
            "version": "1.0.0",
            "capabilities": {}
        }

        # Call the register_agent tool to add the new agent to the server
        result = await client.call_tool("register_agent", {"card": new_card})
        print("Register result:", result)

        # ===== Verify Registration: List AgentCards Again =====
        # The new PlannerAgent should now appear in the resources list
        await list_agent_cards(client)

        # ===== Deregister the AgentCard =====
        # Remove the PlannerAgent we just added
        dereg_result = await client.call_tool("deregister_agent", {"name": "PlannerAgent"})
        print("Deregister result:", dereg_result)

        # ===== Verify Deregistration: Final List =====
        # The PlannerAgent should no longer appear in the resources list
        await list_agent_cards(client)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())