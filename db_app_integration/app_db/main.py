from fastapi import FastAPI
#Local Session
from app_db.db.session import engine
#Base
from app_db.db.base import Base

#routers
from app_db.api import users, profiles, orders

app = FastAPI()

#User
app.include_router(users.router)
#Profile
app.include_router(profiles.router)
#Order
app.include_router(orders.router)

Base.metadata.create_all(bind=engine)