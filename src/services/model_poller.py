import asyncio
import logging
from typing import Type, Callable

from beanie import Document
from beanie.odm.operators.find.comparison import GT

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
        self.last_monotonic_key = cacher_path + f"{model_class.__name__}:last_monotonic_key"

    async def run(self, queue: asyncio.Queue):
        cacher = await get_cacher()

        if cacher is None:
            raise ValueError("Cacher not initialized")

        while True:
            while True:
                last_monotonic = await cacher.get(self.last_monotonic_key)

                if not last_monotonic:
                    last_monotonic = 0

                query = GT(self.model_class.monotonic_seq, last_monotonic)

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
                last_monotonic = last_doc.monotonic_seq

                await cacher.set(
                    self.last_monotonic_key,
                    last_monotonic,
                    expire=None,
                    raise_exc=True
                )

                for d in docs:
                    await queue.put(self.transformer(d))

                if len(docs) < self.batch_size:
                    break

            await asyncio.sleep(self.interval)
