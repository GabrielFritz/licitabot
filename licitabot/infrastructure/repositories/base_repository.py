from typing import List, Optional, Type
from licitabot.application.interfaces.repository import EntityId, Repository, D, T


class BaseRepository(Repository[T, D]):
    pydantic_model: Type[D]
    tortoise_model: Type[T]
    pk_field: str
    related_fields: List[str] = []
    prefetch_fields: List[str] = []

    async def get_all(self, mode: str = "pydantic") -> List[D | T]:
        query = self.tortoise_model.all()
        if self.related_fields:
            query = query.select_related(*self.related_fields)
        if self.prefetch_fields:
            query = query.prefetch_related(*self.prefetch_fields)
        rows = await query.values()
        if mode == "pydantic":
            return [self.pydantic_model.model_validate(row) for row in rows]
        elif mode == "tortoise":
            return rows
        else:
            raise ValueError(f"Invalid mode: {mode}")

    async def get_by_id(self, id: EntityId, mode: str = "pydantic") -> Optional[D | T]:
        query = self.tortoise_model.filter(**{self.pk_field: id})
        if self.related_fields:
            query = query.select_related(*self.related_fields)
        if self.prefetch_fields:
            query = query.prefetch_related(*self.prefetch_fields)
        row = await query.first()
        if mode == "pydantic":
            return self.pydantic_model.model_validate(row) if row else None
        elif mode == "tortoise":
            return row
        else:
            raise ValueError(f"Invalid mode: {mode}")

    async def create(self, entity: D) -> None:
        await self.tortoise_model.create(**entity.model_dump())

    async def update(self, entity: D) -> None:
        data = entity.model_dump()
        data.pop(self.pk_field, None)
        await self.tortoise_model.filter(
            **{self.pk_field: getattr(entity, self.pk_field)}
        ).update(**data)

    async def delete(self, entity: D) -> None:
        await self.tortoise_model.filter(
            **{self.pk_field: getattr(entity, self.pk_field)}
        ).delete()

    async def save(self, entity: D) -> None:
        pk_value = getattr(entity, self.pk_field)
        exists = await self.tortoise_model.filter(**{self.pk_field: pk_value}).exists()
        if exists:
            await self.update(entity)
        else:
            await self.create(entity)

    async def upsert(self, entity: D) -> None:
        await self.save(entity)
