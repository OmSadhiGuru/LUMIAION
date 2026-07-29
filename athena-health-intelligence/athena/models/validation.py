"""Shared vocabulary and result types for the validation engine.

The Literal types here are intentionally closed (unlike source.py) —
these are ATHENA's own internal classification, not an open-ended
external vocabulary, so a typo should fail loudly rather than silently
storing an unrecognized status.
"""

from __future__ import annotations

from typing import Literal

MeasurementType = Literal[
    "measured",
    "device_estimated",
    "calculated",
    "manual",
    "inferred",
    "unverified",
]

ValidationStatus = Literal[
    "valid",
    "questionable",
    "invalid",
    "unverified",
]

DuplicateStatus = Literal[
    "unique",
    "duplicate",
    "possible_duplicate",
]


class ValidationMessage:
    """A single finding from the validation engine, kept as a plain string
    in CanonicalHealthRecord.validation_messages but constructed via this
    helper so the format stays consistent across ranges/consistency/anomalies.
    """

    def __init__(self, check: str, severity: ValidationStatus, detail: str):
        self.check = check
        self.severity = severity
        self.detail = detail

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.check}: {self.detail}"

    def __repr__(self) -> str:
        return f"ValidationMessage({self.check!r}, {self.severity!r}, {self.detail!r})"
