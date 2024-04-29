import asyncio
from contextlib import asynccontextmanager
from services import load_data


@asynccontextmanager
async def app_lifespan(_):

    asyncio.create_task(load_data.load_starter_data())
    # another task for text analysis may be necessary.
    yield
