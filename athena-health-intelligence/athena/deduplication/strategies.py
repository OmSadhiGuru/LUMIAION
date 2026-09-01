"""Pluggable duplicate-matching strategies.

A strategy answers one question: given a candidate record and a list of
existing records for the same metric_type, which (if any) is a
duplicate? Different metric types warrant different tolerances — a
step count from two sources rarely matches exactly, while a manually
re-entered body weight usually does.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import timedelta

from athena.models.canonical import CanonicalHealthRecord


class DedupStrategy(ABC):
    @abstractmethod
    def find_duplicate(
        self, candidate: CanonicalHealthRecord, existing: list[CanonicalHealthRecord]
    ) -> CanonicalHealthRecord | None:
        ...


class TimeWindowValueStrategy(DedupStrategy):
    """Duplicate if same metric_type, start_time within `window`, and
    normalized_value within `value_tolerance` (relative) of each other.
    Non-numeric values fall back to exact equality.
    """

    def __init__(self, window: timedelta = timedelta(minutes=2), value_tolerance: float = 0.01):
        self.window = window
        self.value_tolerance = value_tolerance

    def find_duplicate(
        self, candidate: CanonicalHealthRecord, existing: list[CanonicalHealthRecord]
    ) -> CanonicalHealthRecord | None:
        for other in existing:
            if other.id == candidate.id:
                continue
            if other.metric_type != candidate.metric_type:
                continue
            if abs((other.start_time - candidate.start_time).total_seconds()) > self.window.total_seconds():
                continue
            if not self._values_match(candidate.normalized_value, other.normalized_value):
                continue
            return other
        return None

    def _values_match(self, a, b) -> bool:
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            if a == 0 and b == 0:
                return True
            denom = max(abs(a), abs(b), 1e-9)
            return abs(a - b) / denom <= self.value_tolerance
        return a == b
