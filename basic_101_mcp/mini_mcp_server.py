import json
import logging
from pathlib import Path
from typing import TypedDict

from fastmcp import FastMCP
from mcp.types import Resource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGISTRY_PATH = Path("agents_registry.json")

class AgentCard(TypedDict):
    """Type definition for an AgentCard."""

    name: str
    url: str
    description: str | None
    version: str | None


def load_registry() -> dict[str, AgentCard]:
    """Load the agent registry from disk.

    Returns:
        Dictionary mapping agent names to their AgentCard data.
        Returns empty dict if file doesn't exist.

    Raises:
        json.JSONDecodeError: If registry file contains invalid JSON.
        OSError: If file cannot be read.
    """
    if not REGISTRY_PATH.exists():
        return {}

    try:
        with REGISTRY_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse registry file: {e}")
        raise
    except OSError as e:
        logger.error(f"Failed to read registry file: {e}")
        raise


def save_registry(reg: dict[str, AgentCard]) -> None:
    """Save the agent registry to disk.

    Uses atomic write pattern (write to temp, then rename) to prevent
    corruption on failure.

    Args:
        reg: Dictionary mapping agent names to their AgentCard data.

    Raises:
        OSError: If file cannot be written.
        json.JSONEncodeError: If registry data cannot be serialized.
    """
    temp_path = REGISTRY_PATH.with_suffix(".tmp")
    try:
        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(reg, f, indent=2, ensure_ascii=False)
        temp_path.replace(REGISTRY_PATH)
    except (OSError, json.JSONEncodeError) as e:
        logger.error(f"Failed to save registry: {e}")
        if temp_path.exists():
            temp_path.unlink()
        raise

mcp = FastMCP("AgentCardServer")

# ---------------- Resources ----------------
@mcp.resource("agent://{name}", tags={"public"}, mime_type="application/json")
def get_agent_card(name: str) -> dict:
    """Return the AgentCard JSON for a given agent name.
    Args:
        name: The name of the agent to retrieve.
    Returns:
        The AgentCard data for the requested agent.
        • 	When a client calls 'resources/list', the server will return each concrete AgentCard.
        • 	When a client calls a concrete URI (e.g. agent://PlannerAgent) the server will return the actual JSON.) to fetch the actual AgentCard JSON.        
    Raises:
        ValueError: If the agent name is not found in the registry.
    """
    reg = load_registry()
    if name not in reg:
        logger.warning(f"Agent '{name}' not found in registry")
        raise ValueError(f"Unknown agent {name}")
    return reg[name]

def register_agent_resources():
    reg = load_registry()
    if reg is None:
        return
    for name, card in reg.items():
        def make_reader(card_data):
            def reader() -> dict:
                return card_data
            return reader

        mcp.add_resource_fn(
            make_reader(card),
            f"agent://{name}",
            name=name,
            description=card.get("description", ""),
            mime_type="application/json",
            tags={"public"},
        )

# Call once at startup
register_agent_resources()

# ---------------- Tools ----------------
@mcp.tool()
def register_agent(card: dict) -> str:
    """
    Register a new AgentCard into the registry and MCP resources.
    Args:
        card: Dictionary containing agent information. Must include 'name'
              and 'url' fields at minimum.
    Returns:
        Success message with the registered agent name.
    Raises:
        ValueError: If required fields ('name', 'url') are missing.
        OSError: If registry cannot be saved.
    """
    if "name" not in card or "url" not in card:
        raise ValueError("AgentCard must include 'name' and 'url'")

    try:
        reg = load_registry()
        reg[card["name"]] = card
        save_registry(reg)

        logger.info(f"Registered agent: {card['name']}")
        return f"Registered {card['name']}"
    except Exception as e:
        logger.error(f"Failed to register agent '{card.get('name')}': {e}")
        raise


@mcp.tool()
def deregister_agent(name: str) -> str:
    """
    Remove an AgentCard from the registry and MCP resources.
    Args:
        name: The name of the agent to deregister.
    Returns:
        Success message indicating whether agent was deregistered or not found.
    """
    try:
        reg = load_registry()
        if name in reg:
            reg.pop(name)
            save_registry(reg)
            # uri = f"agent://{name}"
            #if uri in mcp.resources:
            #    del mcp.resources[uri]
            logger.info(f"Deregistered agent: {name}")
            return f"Deregistered {name}"

        logger.warning(f"Agent '{name}' not found for deregistration")
        return f"{name} not found"
    except Exception as e:
        logger.error(f"Failed to deregister agent '{name}': {e}")
        raise

# ---------------- Run ----------------
if __name__ == "__main__":
    mcp.run(
        transport="http",   # spec‑aligned Streamable HTTP transport
        host="127.0.0.1",
        port=8080,
        path="/mcp"         # endpoint is http://127.0.0.1:8080/mcp
    )