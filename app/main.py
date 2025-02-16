from fastapi import FastAPI
from contextlib import asynccontextmanager
from redis.asyncio import Redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(host="localhost", port=6379)
    yield
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "redis": await app.state.redis.ping()
    }