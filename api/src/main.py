from fastapi import FastAPI, Response, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
import aioredis
from . import settings
from .cache import PUB_SUB
from .models import Notification

app = FastAPI()
X_API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await PUB_SUB.connect()


@app.on_event("shutdown")
async def shutdown():
    await PUB_SUB.disconnect()


async def authenticate(x_api_key: str = Depends(X_API_KEY_HEADER)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return True


@app.post("/api/notifications/")
async def send_notification(
    notification: Notification, is_authenticated: bool = Depends(authenticate)
):
    await PUB_SUB.pool.publish_json(notification.user_id, notification.dict())
    return Response(status_code=status.HTTP_201_CREATED)
