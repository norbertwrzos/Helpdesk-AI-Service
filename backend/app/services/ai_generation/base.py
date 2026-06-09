from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.ai_generation.schemas import (
    TicketResponseGenerationInput,
    TicketResponseGenerationResult,
)


class BaseAIResponseProvider(ABC):
    provider_name = "base"

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @abstractmethod
    def generate_ticket_response(
        self,
        data: TicketResponseGenerationInput,
    ) -> TicketResponseGenerationResult:
        raise NotImplementedError