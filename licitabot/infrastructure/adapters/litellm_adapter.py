from licitabot.settings import settings
from httpx import AsyncClient
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from licitabot.infrastructure.adapters.dtos import (
    LiteLLMEmbeddingsParamsDTO,
    LiteLLMEmbeddingsResultDTO,
)


class LiteLLMAdapter:

    def __init__(self):
        self.client = AsyncClient(
            timeout=settings.http.timeout, base_url=settings.litellm.base_url
        )
        self.embeddings_url = "/v1/embeddings"
        self.headers = {
            "Authorization": f"Bearer {settings.litellm.api_key}",
            "Content-Type": "application/json",
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        retry=retry_if_exception_type((Exception,)),
        reraise=True,
    )
    async def get_embeddings(
        self, params: LiteLLMEmbeddingsParamsDTO
    ) -> LiteLLMEmbeddingsResultDTO:
        payload = params.model_dump()
        if not isinstance(payload.get("input"), str):
            raise ValueError("input must be a string")
        resp = await self.client.post(
            self.embeddings_url,
            headers=self.headers,
            json=payload,
        )
        resp.raise_for_status()
        return LiteLLMEmbeddingsResultDTO.model_validate(resp.json())
