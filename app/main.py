from fastapi import FastAPI
from contextlib import asynccontextmanager
from redis.asyncio import Redis
from starlette.middleware.cors import CORSMiddleware

from app.routers import ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(host="localhost", port=6379)
    yield
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ws.router, prefix="/ws")

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "redis": await app.state.redis.ping()
    }