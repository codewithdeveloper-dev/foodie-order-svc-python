from models.models import *
from schemas.schemas import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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
        return JSONResponse(content={"error": str(error)}, status_code=500)
    


@router.post('/order')
async def order(request:OrderItems):
    try:
        user=request.user_id
        cart_items=await CartItem.filter(user_id=user).values()
        if cart_items:
            order=await Order.create(
                user_id=user
            )
            for item in cart_items:
                await OrderItem.create(
                    order=order,
                    item_id=item.get('food_id'),
                    quantity=item.get('quantity'),
                    price=120.00
                )
            
            payment=await paymentResponse(order_id=order.id,user_id=user)
            if payment.get("status") == "success":
                await Order.filter(id=order.id).update(status="Success")
                await CartItem.filter(user_id=user).delete()
                location = "Chennai"
                assigned = await assignDeliveryPerson(order.id, user, location)

                if assigned:
                    message = "Order placed and delivery person has been assigned!"
                else:
                    message = "Order placed but no delivery person available right now."

                return JSONResponse(
                    content={"order_id": order.id, "message": message},
                    status_code=201
                )
            else:
                return JSONResponse(
                content={"message": "Payment failed. Order not placed."},
                status_code=400
            )

              
        else:
               return JSONResponse(content={"response":jsonable_encoder({"message": "Oops! No items left in the cart. Please add some items to order :)"})}, media_type="application/json",status_code=200)
    except Exception as  error:
        return JSONResponse(content={"error": str(error)}, status_code=500)
    


async def paymentResponse(order_id, user_id):
    return {"status": "success"}



async def assignDeliveryPerson(order_id, user, location):
    try:
        available_person = await DeliveryPerson.filter(is_available=True, location=location).first()
        if available_person:
            await DeliveryAssignment.create(
                delivery_person=available_person,
                order_id=order_id
            )
            await DeliveryPerson.filter(id=available_person.id).update(is_available=False)
            
            return True
        return False
    except Exception as error:
        return False