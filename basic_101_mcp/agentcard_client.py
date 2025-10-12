import asyncio
from fastmcp import Client

async def main():
    client = Client("http://127.0.0.1:8080/mcp")

    async with client:
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

if __name__ == "__main__":
    asyncio.run(main())