import asyncio
from licitabot.infrastructure.adapters.litellm_adapter import LiteLLMAdapter
from licitabot.infrastructure.adapters.dtos import LiteLLMEmbeddingsParamsDTO


async def main():
    adapter = LiteLLMAdapter()
    params = LiteLLMEmbeddingsParamsDTO(input="Hello, world!")
    result = await adapter.get_embeddings(params)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
