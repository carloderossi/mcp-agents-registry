import asyncio
from fastmcp import Client

async def main():
    client = Client("http://127.0.0.1:8080/mcp")

    async with client:
        # Deregister the AgentCard
        dereg_result = await client.call_tool("deregister_agent", {"name": "PlannerAgent"})
        print("Deregister result:", dereg_result)

if __name__ == "__main__":
    asyncio.run(main())