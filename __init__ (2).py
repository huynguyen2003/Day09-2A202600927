"""Shared LLM factory for all agents.

Uses Gemini directly when GEMINI_API_KEY is configured. Otherwise falls
back to OpenRouter as an OpenAI-compatible API.
"""

import os

from langchain_openai import ChatOpenAI


def get_llm() -> ChatOpenAI:
    """Return a ChatOpenAI-compatible client for Gemini or OpenRouter."""
    max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()

    if gemini_key and gemini_key not in {"your_gemini_api_key_here", "your_key_here"}:
        return ChatOpenAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            openai_api_key=gemini_key,
            openai_api_base=os.getenv(
                "GEMINI_BASE_URL",
                "https://generativelanguage.googleapis.com/v1beta/openai/",
            ),
            max_tokens=max_tokens,
        )

    return ChatOpenAI(
        model=os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4-5"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=max_tokens,
    )
