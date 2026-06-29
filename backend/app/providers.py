import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .config import Settings


class ProviderError(Exception):
    pass


@dataclass
class ProviderResult:
    raw: str


class BriefProvider(ABC):
    @abstractmethod
    def decode(self, text: str, mode: str = "normal") -> ProviderResult:
        raise NotImplementedError


class FakeBriefProvider(BriefProvider):
    def decode(self, text: str, mode: str = "normal") -> ProviderResult:
        if mode == "provider_failure":
            raise ProviderError("Fake provider failed")
        if mode == "malformed_json":
            return ProviderResult(raw='{"summary": "broken",')
        if mode == "missing_fields":
            return ProviderResult(raw=json.dumps({"summary": "Missing required fields"}))
        if mode == "bad_severity":
            return ProviderResult(
                raw=json.dumps(
                    {
                        "summary": "Brief about a landing page",
                        "goals": ["Explain the product", "Collect emails"],
                        "deliverables": ["Landing page", "Copy suggestions"],
                        "constraints": ["Limited budget", "Two-week timeline"],
                        "risks": [
                            {
                                "risk": "Timeline may be tight",
                                "severity": "urgent",
                                "reason": "Design, copy and SEO are requested together",
                            }
                        ],
                        "clarifying_questions": ["What pricing model should be shown?"],
                        "recommended_next_action": "Confirm scope and prepare a page outline",
                    }
                )
            )

        normalized = " ".join(text.strip().split())
        return ProviderResult(
            raw=json.dumps(
                {
                    "summary": normalized[:180],
                    "goals": [
                        "Clarify the client request",
                        "Turn the brief into an actionable delivery plan",
                    ],
                    "deliverables": [
                        "Normalized brief summary",
                        "Goal and deliverable list",
                        "Risk assessment",
                        "Clarifying questions",
                    ],
                    "constraints": [
                        "Use only information present in the brief",
                        "Keep recommendations concise",
                    ],
                    "risks": [
                        {
                            "risk": "Scope may be broader than the available timeline",
                            "severity": "medium",
                            "reason": "The brief mentions several workstreams that need coordination",
                        }
                    ],
                    "clarifying_questions": [
                        "Who is the primary audience?",
                        "What outcome defines success?",
                        "Are there brand or technical constraints?",
                    ],
                    "recommended_next_action": "Confirm scope, timeline and acceptance criteria before estimating.",
                }
            )
        )


class OpenAIBriefProvider(BriefProvider):
    def __init__(self, settings: Settings):
        self.settings = settings

    def decode(self, text: str, mode: str = "normal") -> ProviderResult:
        raise ProviderError("Real OpenAI provider is documented but not enabled in this prototype")


def get_provider(settings: Settings) -> BriefProvider:
    if settings.llm_provider == "fake":
        return FakeBriefProvider()
    if settings.llm_provider == "openai":
        return OpenAIBriefProvider(settings)
    raise ProviderError("Unsupported provider")
