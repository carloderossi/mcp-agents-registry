# mini_mcp_client.py
import asyncio
import json
import sys

async def main():
    # Connect to the already-running server via stdio
    # (here we just spawn it again for demo, but you can connect pipes/sockets)
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "mini_fastmcp_server.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )

    # 1. List tools
    list_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    proc.stdin.write((json.dumps(list_req) + "\n").encode())
    await proc.stdin.drain()
    line = await proc.stdout.readline()
    print("ListTools response:", line.decode().strip())

    # 2. Call the echo tool
    call_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "echo",
            "arguments": {"text": "hello mcp"}
        }
    }
    proc.stdin.write((json.dumps(call_req) + "\n").encode())
    await proc.stdin.drain()
    line = await proc.stdout.readline()
    print("CallTool response:", line.decode().strip())

    proc.kill()

if __name__ == "__main__":
    asyncio.run(main())