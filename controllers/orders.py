from models.models import *
from schemas.schemas import *
from fastapi.responses import JSONResponse
from fastapi import APIRouter

router=APIRouter(prefix="/v1")


@router.post("/add-to-cart/")
async def add_to_cart(request: AddToCart):
    try:
        cart = await CartItem.create(
            food_id=request.food_id,
            user_id=request.user_id,
        )
        return JSONResponse(
            content={"message": "Food added to cart"}, media_type="application/json",status_code=201
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




@router.patch('/cart/update')
async def updateItemsQuantity(request:UpdateQuantity):
    try:
        updateQuantity=await CartItem.filter(
            user_id=request.user_id,
            food_id=request.food_id
        ).update(quantity=request.quantity)

        if updateQuantity:
           return JSONResponse(content={"response":"Successfully updated"}, media_type="application/json",status_code=202)
        else:
            return JSONResponse(content={"response":"oops!! item not found"}, media_type="application/json",status_code=404)
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=500)
    

@router.delete('/cart/remove/{item_id}')
async def removeItemsFromCart(item_id:int):
    try:
        removeFromCart=await CartItem.filter(food_id=item_id).delete()
        if removeFromCart:
            return JSONResponse(content={"response":"Successfully removed"}, media_type="application/json",status_code=200)
        else:
            return JSONResponse(content={"response":"oops!! item not found"}, media_type="application/json",status_code=404)
    except Exception as error:
        return JSONResponse(content={"error": str(e)}, status_code=500)