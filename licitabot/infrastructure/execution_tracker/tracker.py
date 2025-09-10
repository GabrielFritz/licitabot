import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from licitabot.infrastructure.execution_tracker.models import Execution
from licitabot.infrastructure.database.session import create_session
import functools
import inspect


class ExecutionTracker:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def start(self, job_name: str, meta: dict | None = None) -> Execution:

        execution = Execution(job_name=job_name, meta=meta)
        self.session.add(execution)
        await self.session.commit()
        return execution

    async def mark_success(
        self, execution: Execution, result: dict | None = None
    ) -> None:
        execution.mark_success(result)
        await self.session.commit()

    async def mark_failed(
        self, execution: Execution, error: dict | None = None
    ) -> None:
        execution.mark_failed(error)
        await self.session.commit()

    async def mark_cancelled(self, execution: Execution) -> None:
        execution.mark_cancelled()
        await self.session.commit()


async def get_execution_tracker():
    session = await create_session()
    async with session:
        return ExecutionTracker(session=session)


def _convert_to_dict(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    elif hasattr(value, "dict"):
        return value.dict()
    else:
        return str(value)


def track(job_name: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            tracker = await get_execution_tracker()
            signature = inspect.signature(func)
            bound = signature.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            meta = {}
            for name, value in bound.arguments.items():
                if name != "self":
                    try:
                        meta[name] = _convert_to_dict(value)
                    except Exception:
                        meta[name] = str(value)

            execution = await tracker.start(job_name, meta)

            try:
                result = await func(*args, **kwargs)
                await tracker.mark_success(
                    execution, {"result": _convert_to_dict(result)}
                )
                return result
            except asyncio.CancelledError:
                await tracker.mark_cancelled(execution)
                raise
            except Exception as e:
                await tracker.mark_failed(execution, {"error": str(e)})
                raise e

        return wrapper

    return decorator
