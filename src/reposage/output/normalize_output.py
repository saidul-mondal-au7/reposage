"""
Shared helpers to normalize CrewAI task outputs
into predictable Python structures.
"""

from typing import Any
from pydantic import BaseModel


def normalize_output(obj: Any):
    """
    Normalize CrewAI task outputs into plain Python types.

    Handles:
    - Pydantic v1 & v2 models
    - dict
    - list
    - primitives
    """

    if obj is None:
        return None

    # Pydantic v2
    if isinstance(obj, BaseModel):
        return obj.model_dump()

    # dict → recurse
    if isinstance(obj, dict):
        return {k: normalize_output(v) for k, v in obj.items()}

    # list → recurse
    if isinstance(obj, list):
        return [normalize_output(i) for i in obj]

    # primitives (str, int, float, bool)
    return obj

