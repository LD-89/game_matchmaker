import asyncio

from fastapi import APIRouter, WebSocket

from services.matchmaking import MatchmakingService

PLAYERS_COUNT = 2

router = APIRouter()
mm_service = MatchmakingService()

@router.websocket("/match/queue")
async def websocket_queue(websocket: WebSocket):
    await websocket.accept()
    try:
        token = await websocket.receive_text()
        ## TODO implement JWT authentication
        player_data = parse_jwt(token)

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
    except Exception as e:
        await websocket.close(code=1011)