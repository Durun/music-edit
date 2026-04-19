"""MCP server entry point. Tools will be implemented in Phase 1+."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("music-edit-mcp")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
