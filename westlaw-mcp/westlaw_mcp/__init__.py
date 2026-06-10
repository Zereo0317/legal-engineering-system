"""Westlaw MCP Server — unified legal research across multiple sources."""

__version__ = "0.1.0"

def main():
    from .server import mcp
    mcp.run()
