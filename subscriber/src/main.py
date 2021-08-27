from typing import Optional
import jwt
import asyncio
from aioredis.pubsub import Receiver
import aioredis
from starlette.websockets import WebSocketState
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    Cookie,
    status,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware
from . import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def authenticate(access_jwt: str):
    try:
        payload = jwt.decode(
            access_jwt,
            settings.JWT.SIGNING_KEY,
            algorithms=["HS256"],
            options=settings.JWT.DECODE_OPTIONS,
        )
    except (
        jwt.exceptions.ExpiredSignatureError,
        jwt.exceptions.InvalidTokenError,
    ) as e:
        print(e)
        return None

    return payload["user_id"]


@app.websocket("/notifications/")
async def websocket_endpoint(
    websocket: WebSocket,
    access_jwt: Optional[str] = Cookie(...),
):
    user_id = await authenticate(access_jwt)
    try:
        connection = await aioredis.create_redis(settings.Redis.URL)
        mpsc = Receiver()
        await connection.psubscribe(mpsc.pattern(f"{user_id}"))
        await websocket.accept()

        while True:
            _, (channel, message) = await asyncio.wait_for(
                mpsc.get(encoding="utf-8"), timeout=12000
            )
            await websocket.send_json(message)

    # TODO: close websockets with different exceptions codes.
    except (WebSocketDisconnect, asyncio.exceptions.TimeoutError):
        pass
    except Exception as e:
        raise e
    finally:
        await connection.punsubscribe(f"{user_id}")
        mpsc.stop()
        connection.close()
        await connection.wait_closed()
        if websocket.application_state is not WebSocketState.DISCONNECTED:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
