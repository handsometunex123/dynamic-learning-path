"""
LLM Agent module — wraps OpenAI's chat API for the tutor and companion.

Falls back to pre-written DEMO_MODE responses if OPENAI_API_KEY is not set.
"""
from __future__ import annotations
import os
from typing import List, Dict

from dotenv import load_dotenv

from core.course_data import DEMO_TUTOR_RESPONSES, DEMO_COMPANION_RESPONSE

load_dotenv()

_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEMO_MODE = not bool(_API_KEY)

if not DEMO_MODE:
    from openai import OpenAI
    _client = OpenAI(api_key=_API_KEY)


def _chat(messages: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Send a chat completion request and return the assistant content."""
    resp = _client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=600,
    )
    return resp.choices[0].message.content.strip()


# ── Tutor Agent ───────────────────────────────────────────────────────────────

_TUTOR_SYSTEM = {
    "beginner": (
        "You are a friendly, patient Python programming tutor helping a beginner. "
        "ALWAYS give a hint first before explaining the answer. Use simple language, "
        "avoid jargon, and include a short code example. Keep responses under 200 words."
    ),
    "intermediate": (
        "You are a Python tutor helping an intermediate student. Be direct and technical. "
        "Explain the WHY behind the behaviour, not just the fix. Reference relevant Python "
        "concepts (scope, mutability, etc.). Keep responses under 200 words."
    ),
    "advanced": (
        "You are a Python expert assisting an advanced student. Discuss CPython internals, "
        "performance implications, and idiomatic patterns where relevant. Be concise and "
        "assume familiarity with the language. Keep responses under 220 words."
    ),
}


def tutor_respond(
    question: str,
    code: str,
    level: str,
    history: List[Dict],
) -> str:
    """
    Generate a tutor response.

    history: list of prior {"role": ..., "content": ...} messages.
    """
    level_key = level.lower()
    if DEMO_MODE:
        return DEMO_TUTOR_RESPONSES.get(level_key, DEMO_TUTOR_RESPONSES["beginner"])

    system_msg = {"role": "system", "content": _TUTOR_SYSTEM[level_key]}
    user_content = question
    if code.strip():
        user_content = f"My code:\n```python\n{code}\n```\n\n{question}"

    messages = [system_msg] + history + [{"role": "user", "content": user_content}]
    return _chat(messages)


# ── Course Companion Agent ────────────────────────────────────────────────────

_COMPANION_SYSTEM = (
    "You are a helpful teaching assistant. Your knowledge comes ONLY from the course "
    "material excerpt provided below. Answer the student's question using only that "
    "material. If the answer isn't in the excerpt, say so clearly.\n\n"
    "Always cite the relevant part of the material in your answer. "
    "Keep responses under 200 words."
)


def companion_respond(
    question: str,
    course_excerpt: str,
    history: List[Dict],
) -> str:
    """
    Generate a course-companion response grounded in the provided excerpt.
    Simulates a fine-tuned SLM by injecting course material as context.
    """
    if DEMO_MODE:
        return DEMO_COMPANION_RESPONSE

    system_msg = {
        "role": "system",
        "content": _COMPANION_SYSTEM + f"\n\n--- COURSE MATERIAL ---\n{course_excerpt}",
    }
    messages = [system_msg] + history + [{"role": "user", "content": question}]
    return _chat(messages)
