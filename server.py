from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.config import init_db, close_up
from controllers.orders import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield

    await close_up()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():

    return {"response": ""}

app.include_router(router)
