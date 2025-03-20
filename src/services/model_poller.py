import asyncio
import logging
from datetime import datetime
from typing import Type, Callable
from uuid import UUID

from beanie import Document
from beanie.odm.operators.find.comparison import GT, Eq
from beanie.odm.operators.find.logical import Or, And

from db.casher import get_cacher

logger = logging.getLogger(__name__)


class ModelPoller:
    def __init__(
            self,
            model_class: Type[Document],
            transformer: Callable,
            interval: int = 5,
            batch_size: int = 1000
    ):
        self.model_class = model_class
        self.transformer = transformer
        self.interval = interval
        self.batch_size = batch_size

        cacher_path = "UGC_service:src:services:model_poller:"
        self.last_created_at_key = (
                cacher_path + f"{model_class.__name__}:last_created_at"
        )
        self.last_id_key = (
                cacher_path + f"{model_class.__name__}:last_id_key"
        )

    async def run(self, queue: asyncio.Queue):
        cacher = await get_cacher()

        if cacher is None:
            raise ValueError("Cacher not initialized")

        while True:
            while True:
                last_created_at_str = await cacher.get(
                    self.last_created_at_key
                )
                last_id_str = await cacher.get(
                    self.last_id_key
                )

                if not last_created_at_str or not last_id_str:
                    last_created_at = datetime(1970, 1, 1)
                    last_id = UUID(int=0)
                else:
                    last_created_at = datetime.fromisoformat(
                        last_created_at_str
                    )
                    last_id = UUID(last_id_str)

                query = Or(
                    GT(
                        self.model_class.created_at, last_created_at
                    ),
                    And(
                        Eq(
                            self.model_class.created_at, last_created_at
                        ),
                        GT(
                            self.model_class.id, last_id
                        ),
                    ),
                )

                docs = await (
                    self.model_class.find(query).sort(
                        [
                            (self.model_class.created_at, 1),
                            (self.model_class.id, 1),
                        ]
                    ).limit(self.batch_size).to_list(self.batch_size)
                )

                if not docs:
                    break

                last_doc = docs[-1]
                new_created_at = last_doc.created_at
                new_id = last_doc.id

                await cacher.set(
                    self.last_created_at_key,
                    new_created_at.isoformat(),
                    expire=None,
                    raise_exc=True
                )
                await cacher.set(
                    self.last_id_key,
                    str(new_id),
                    expire=None,
                    raise_exc=True
                )

                for d in docs:
                    await queue.put(self.transformer(d))

                if len(docs) < self.batch_size:
                    break

            await asyncio.sleep(self.interval)
