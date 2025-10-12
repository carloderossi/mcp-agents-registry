# mini_mcp_client.py
import asyncio
import json
from fastmcp import Client

async def list_agent_cards(client):
        # List resources (AgentCards)
        resources = await client.list_resources()
        print("Resources:")
        for r in resources:
            print(f" - {r.uri} ({r.name})")

        # Retrieve and print each AgentCard as formatted JSON
        print("\nAgentCards:")
        for r in resources:
            content = await client.read_resource(r.uri)
            # content is a list of Content objects; each may have .text
            for c in content:
                if hasattr(c, "text") and c.text:
                    try:
                        card = json.loads(c.text)
                        print(f"\n{r.uri}:")
                        print(json.dumps(card, indent=2))
                    except json.JSONDecodeError:
                        print(f"\n{r.uri}:")
                        print(c.text)

async def main():
    client = Client("http://127.0.0.1:8080/mcp")
    
    async with client:
        await list_agent_cards(client)   

        # List tools
        tools = await client.list_tools()
        print("\nTools:")
        for t in tools:
            print(f"\n - {t.name}: {t.description}\n ")
        
        # Register a new AgentCard
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

        result = await client.call_tool("register_agent", {"card": new_card})
        print("Register result:", result)
        
        await list_agent_cards(client)
        
        # Deregister the AgentCard
        dereg_result = await client.call_tool("deregister_agent", {"name": "PlannerAgent"})
        print("Deregister result:", dereg_result)

        await list_agent_cards(client)

if __name__ == "__main__":
    asyncio.run(main())