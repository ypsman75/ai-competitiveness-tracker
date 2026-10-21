"""Source-specific fetchers. Each returns rows in the canonical schema."""

import requests

TIMEOUT = 60
USER_AGENT = "ai-competitiveness-tracker (+https://github.com/ypsman75/ai-competitiveness-tracker)"


def get(url: str, **kwargs) -> requests.Response:
    headers = {"User-Agent": USER_AGENT, **kwargs.pop("headers", {})}
    response = requests.get(url, headers=headers, timeout=TIMEOUT, **kwargs)
    response.raise_for_status()
    return response
