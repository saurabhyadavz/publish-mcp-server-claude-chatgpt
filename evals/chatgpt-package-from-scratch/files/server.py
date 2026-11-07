"""Habitat's MCP server (shortened). Deployed at https://api.habitat-example.com/mcp."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Habitat",
    instructions=(
        "Habitat keeps the habits a user logs. Use log_habit when they say they did a habit, "
        "get_streak for how long a run is, and list_habits to see what they track."
    ),
)

READ = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
WRITE = {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False}


@mcp.tool(title="List my habits", annotations=READ)
def list_habits() -> list[dict]:
    """The habits the signed-in user tracks, with today's status."""
    ...


@mcp.tool(title="Log a habit", annotations=WRITE)
def log_habit(habit: str, date: str | None = None) -> dict:
    """Record that the user did a habit, today unless a date (YYYY-MM-DD) is given."""
    ...


@mcp.tool(title="Get a streak", annotations=READ)
def get_streak(habit: str) -> dict:
    """How many days in a row the user has done this habit, and their best run."""
    ...


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
