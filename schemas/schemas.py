from pydantic import BaseModel



class AddToCart(BaseModel):
    food_id: int
    user_id:int