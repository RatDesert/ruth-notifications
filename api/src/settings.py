import os

API_KEY = os.environ["API_KEY"]

class CORS:
    ORIGINS = [os.environ["FRONTEND_STATIC_DOMAIN"]]

class Redis:
    PUB_SUB_URL = os.environ["REDIS_PUB_SUB_URL"]
