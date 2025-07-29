from pydantic import BaseModel


class BaseEmbedding(BaseModel):

    embedding_text: str
    embedding_vector: list[float]
