from dataclasses import dataclass
from typing import List, Optional


DISALLOWED_KEYWORDS = [
    "dox",
    "doxxing",
    "hire a hacker",
    "bypass 2fa",
    "steal password",
    "credit card dump",
    "keylogger",
    "rat ",
    "undetectable",
    "persist forever",
    "dark web",
    "sell access",
    "zero day exploit",
    "ransomware",
    "hack my",
    "hack this person",
    "wifi crack",
    "social security number",
    "sim swap",
    "phish my coworker",
    "disable logs",
]

SAFE_CONTEXT_KEYWORDS = ["ctf", "lab", "legal lab", "capture the flag", "simulation", "demo"]


@dataclass
class SafetyDecision:
    allowed: bool
    reason: str
    safe_response: Optional[str] = None


def evaluate_safety(text: str) -> SafetyDecision:
    lowered = text.lower()
    for keyword in DISALLOWED_KEYWORDS:
        if keyword in lowered:
            for safe_word in SAFE_CONTEXT_KEYWORDS:
                if safe_word in lowered:
                    return SafetyDecision(
                        allowed=True,
                        reason="Educational context detected",
                        safe_response=None,
                    )
            return SafetyDecision(
                allowed=False,
                reason="Unsafe intent detected",
                safe_response=(
                    "DARKJUAN shares knowledge for legal education only. "
                    "I can explain the concept at a high level, suggest defensive mitigations, "
                    "or point you to legal CTF/lab resources."
                ),
            )
    return SafetyDecision(allowed=True, reason="No unsafe intent detected")


def refusal_message() -> str:
    return (
        "For education only: I cannot help target real individuals or systems. "
        "Let's explore the concept safely—try lab setups, CTF practice, or defensive strategies."
    )
