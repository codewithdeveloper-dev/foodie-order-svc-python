from tortoise import fields, models
from tortoise.models import Model
from datetime import datetime


class Restaurant(Model):
    restaurant_id = fields.BigIntField(pk=True)
    restaurant_name = fields.CharField(max_length=255)
    cuisine_type = fields.CharField(max_length=100, null=True)
    address = fields.TextField(null=True)
    phone_number = fields.CharField(max_length=15, null=True)
    email = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    
class MenuCategory(Model):
    category_id = fields.BigIntField(pk=True)
    restaurant_id=fields.ForeignKeyField(model_name="models.Restaurant",related_name='categories')
    category_name=fields.CharField(max_length=100,null=True)
    
class SubCategory(Model):
    subcategory_id = fields.BigIntField(pk=True)
    category = fields.ForeignKeyField('models.MenuCategory', related_name='subcategories')
    type = fields.CharField(max_length=50)  
    
    
    
    

class MenuItem(Model):
    item_id = fields.BigIntField(pk=True)
    subcategory = fields.ForeignKeyField('models.SubCategory', related_name='items')
    item_name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    img_url = fields.CharField(max_length=255, null=True)
    status = fields.CharField(max_length=10, default='active') 
    quantity = fields.IntField(default=0)
    spicy_level = fields.CharField(max_length=20, null=True)
    is_available = fields.BooleanField(default=True)
    discount = fields.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    preparation_time = fields.IntField(null=True) 
    rating = fields.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    
    
class AddToCart(Model):
    cart_id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField(null=False)
    food_id= fields.ForeignKeyField('models.MenuItem',related_name='cart')
    

class CartItem(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    food_id = fields.BigIntField()
    quantity = fields.IntField(default=1)
    added_at = fields.DatetimeField(auto_now_add=True)
    
    
    
class Order(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    status = fields.CharField(max_length=20, default='pending')  
    created_at = fields.DatetimeField(auto_now_add=True)



class OrderItem(Model):
    id = fields.BigIntField(pk=True)
    order = fields.ForeignKeyField("models.Order", related_name="items")
    item_id = fields.BigIntField()
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)

    
class DeliveryPerson(Model):  
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100)
    phone_number = fields.CharField(max_length=15, unique=True)
    email = fields.CharField(max_length=100, null=True)
    is_available = fields.BooleanField(default=True)
    location = fields.CharField(max_length=255, null=True)
    rating = fields.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    assigned_orders = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)



class DeliveryAssignment(Model):
    id=fields.BigIntField(pk=True)
    delivery_person_id=fields.ForeignKeyField("models.DeliveryPerson",related_name="delivery_person")
    order=fields.BigIntField()

