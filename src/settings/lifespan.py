from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import engine, Base


@asynccontextmanager
async def init_db(application: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield