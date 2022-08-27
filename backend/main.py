from fastapi import FastAPI
from middleware import initMiddleware
from db import db
from routers import predict

app = FastAPI()

initMiddleware(app)

app.include_router(predict.router)
# app.include_router(preprocess.router)

@app.on_event("startup")
async def startup():
    await db.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()
