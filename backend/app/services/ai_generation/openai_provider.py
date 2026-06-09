from __future__ import annotations

import logging

from app.services.ai_generation.base import BaseAIResponseProvider
from app.services.ai_generation.prompt_builder import (
    build_system_instruction,
    build_user_prompt,
)
from app.services.ai_generation.schemas import (
    StructuredMailResponse,
    TicketResponseGenerationInput,
    TicketResponseGenerationResult,
)

logger = logging.getLogger(__name__)


class OpenAIResponseProvider(BaseAIResponseProvider):
    provider_name = "openai"

    def __init__(
        self,
        api_key: str,
        model_name: str,
        temperature: float,
        max_output_tokens: int,
        client=None,
    ) -> None:
        if not api_key and client is None:
            raise ValueError("OPENAI_API_KEY is not configured.")

        super().__init__(model_name=model_name)
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

        if client is not None:
            self._client = client
            return

        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - depends on runtime environment
            raise RuntimeError("The openai package is required for OpenAI text generation.") from exc

        self._client = OpenAI(api_key=api_key)

    def generate_ticket_response(
        self,
        data: TicketResponseGenerationInput,
    ) -> TicketResponseGenerationResult:
        system_instruction = build_system_instruction(data.agent_name)
        user_prompt = build_user_prompt(data)

        try:
            response = self._client.responses.parse(
                model=self.model_name,
                instructions=system_instruction,
                input=[{"role": "user", "content": user_prompt}],
                text_format=StructuredMailResponse,
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            )
        except Exception as exc:
            logger.warning(
                "OpenAI response generation failed for model '%s': %s",
                self.model_name,
                exc,
            )
            raise RuntimeError("OpenAI response generation failed.") from exc

        parsed = getattr(response, "output_parsed", None)
        raw_response = getattr(response, "output_text", None)
        if parsed is None:
            raise RuntimeError("OpenAI response could not be parsed into the expected schema.")

        return TicketResponseGenerationResult(
            subject=parsed.subject,
            email_body=parsed.email_body,
            confidence=parsed.confidence,
            used_sources=parsed.used_sources,
            requires_human_review=parsed.requires_human_review,
            limitations=parsed.limitations,
            model_name=self.model_name,
            provider_name=self.provider_name,
            raw_response=raw_response,
        )