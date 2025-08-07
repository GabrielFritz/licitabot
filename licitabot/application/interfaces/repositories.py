from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar
from datetime import datetime

T = TypeVar("T")


class RepositoryInterface(Generic[T], ABC):
    @abstractmethod
    async def upsert(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: Any) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def count_all(self) -> int:
        raise NotImplementedError


class RepositoryInterfaceWithGlobalUpdate(RepositoryInterface[T], ABC):
    @abstractmethod
    async def get_by_global_update_between(
        self, data_ini: datetime, data_fim: datetime
    ) -> List[T]:
        raise NotImplementedError
