from tortoise import Tortoise

DB_URL="postgres://postgres:iness123@localhost:5432/foodapp_db"


async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['models.models']}
    )
    
    await Tortoise.generate_schemas()
    

async def close_up():
    await Tortoise.close_connections()
  