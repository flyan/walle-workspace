#!/usr/bin/env python3
"""Simple Xueqiu MCP server using pysnowball."""

import os
import sys

# Set token from environment or config
os.environ['XUEQIUTOKEN'] = os.environ.get('XUEQIUTOKEN', '')

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("xueqiu")

# Import pysnowball modules
import pysnowball as sb
from pysnowball.realtime import quotec, kline
from pysnowball.finance import indicator, balance, income
from pysnowball.index import index_perf_7, index_perf_30

@mcp.tool()
def get_quote(symbols: str) -> dict:
    """Get real-time quote for stock symbols (e.g., 'SH000001, SZ399001')."""
    sb.set_token(os.environ['XUEQIUTOKEN'])
    try:
        return quotec(symbols)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_kline(symbol: str, period: str = "day", count: int = 10) -> dict:
    """Get K-line data for a symbol. period: day/week/month, count: number of periods."""
    sb.set_token(os.environ['XUEQIUTOKEN'])
    try:
        return kline(symbol, period, count)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_financial_data(symbol: str, type: str = "indicator") -> dict:
    """Get financial data. type: indicator/balance/income."""
    sb.set_token(os.environ['XUEQIUTOKEN'])
    try:
        if type == "indicator":
            return indicator(symbol)
        elif type == "balance":
            return balance(symbol)
        elif type == "income":
            return income(symbol)
        else:
            return {"error": f"Unknown type: {type}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_index_performance(period: str = "7") -> dict:
    """Get index performance. period: 7/30/90 days."""
    sb.set_token(os.environ['XUEQIUTOKEN'])
    try:
        if period == "7":
            return index_perf_7()
        elif period == "30":
            return index_perf_30()
        else:
            return {"error": f"Unknown period: {period}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()
    else:
        # Run as stdio server
        mcp.run(transport="stdio")
