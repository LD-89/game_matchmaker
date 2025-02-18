import asyncio
import jwt
from fastapi import APIRouter, WebSocket, Query
from websockets import WebSocketException

from services.matchmaking import MatchmakingService

## TODO move to secrets
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
PLAYERS_COUNT = 2

router = APIRouter()
mm_service = MatchmakingService()

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None

async def ws_auth(token: str = Query(...)):
    payload = verify_token(token)
    if not payload:
        raise WebSocketException(403)
    return payload


@router.websocket("/match/queue")
async def websocket_queue(
        websocket: WebSocket,
        token: str = Query(...)
):
    user_payload = await ws_auth(token)
    await websocket.accept()
    try:
        player_data = {
            "id": user_payload["sub"],
            "elo_rating": user_payload.get("elo_rating", 1000)
        }

        await mm_service.add_to_queue(
            player_id = player_data["id"],
            elo_rating = player_data["elo_rating"],
        )

        while True:
            candidates = await mm_service.find_match(player_data["id"])
            if len(candidates) >= PLAYERS_COUNT:
                await websocket.send_json({
                    "status": "matched",
                    "players": candidates
                })
                break
            await asyncio.sleep(2)
    except WebSocketException as e:
        await websocket.close(code=e.code, reason=str(e))
    except Exception as e:
        await websocket.close(code=1011, reason="Internal server error")