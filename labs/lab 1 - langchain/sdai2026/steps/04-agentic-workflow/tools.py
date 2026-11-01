"""
Tools for step 04, grouped by the node that uses them.
Search and statistics come from the mock API (start it with: uv run services/mock_api.py).
"""

import json

import requests
from langchain_core.tools import tool

from lab.config import MOCK_API_URL


def _get(path: str, **params) -> str:
    """Calls the mock API and returns the JSON as a string (tools should return text for the LLM)."""
    try:
        r = requests.get(f"{MOCK_API_URL}{path}", params=params, timeout=5)
        return json.dumps(r.json())
    except requests.RequestException as e:
        # Never crash inside a tool: return the error so the LLM can react to it
        return f"ERROR: could not reach the API ({e.__class__.__name__}). Is services/mock_api.py running?"


# ---------- researcher tools ----------
@tool
def web_search(query: str) -> str:
    """Searches the web and returns the titles and snippets of the most relevant pages.
    Use short keyword queries, e.g. 'AI medicine diagnosis'."""
    return _get("/api/search", q=query)


@tool
def get_statistics(topic: str) -> str:
    """Returns a time series of statistics about a topic.
    Available topics: 'ai adoption', 'ai devices', 'ai market', 'llm usage students'."""
    return _get("/api/stats", topic=topic)


# ---------- analyst tools ----------
@tool
def calculate_percentage(value: float, total: float) -> float:
    """Calculates what percentage 'value' is of 'total'."""
    if total == 0:
        return 0.0
    return round(value / total * 100, 2)


@tool
def calculate_growth(old_value: float, new_value: float) -> float:
    """Calculates the percentage growth from old_value to new_value."""
    if old_value == 0:
        return 0.0
    return round((new_value - old_value) / old_value * 100, 2)


# ---------- other tools ----------
@tool
def get_weather(city: str) -> str:
    """Returns the current weather (temperature, condition, humidity, wind) for a city."""
    return _get("/api/weather", city=city)
