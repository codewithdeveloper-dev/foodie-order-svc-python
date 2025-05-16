from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from db.config import init_db, close_up
from models.models import *
from schemas.schemas import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield

    await close_up()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():

    return {"response": ""}


@app.post("/v1/add-to-cart/")
async def add_to_cart(request: AddToCart):
    try:
        cart = await CartItem.create(
            food_id=request.food_id,
            user_id=request.user_id,
        )
        return JSONResponse(
            content={"message": "Food added to cart"}, media_type="application/json"
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
