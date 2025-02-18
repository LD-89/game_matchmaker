import asyncio
import pytest
import jwt
from websockets import connect, WebSocketException


@pytest.mark.asyncio
async def test_websocket_connection():
    valid_token = {
        "sub": "test_user",
        "elo_rating": 2000
    }
    uri = f"ws://localhost:8000/ws/match/queue?token={valid_token}"
    async with connect(uri) as websocket:
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=5)
            assert "matched" in response
        except asyncio.TimeoutError:
            pytest.fail("Websocket connection timed out")
        except WebSocketException as e:
            pytest.fail(f"Websocket connection failed: {e}")