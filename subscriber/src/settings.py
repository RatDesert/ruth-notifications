import os


class CORS:
    ORIGINS = [os.environ["FRONTEND_STATIC_DOMAIN"]]

class Redis:
    URL = os.environ["REDIS_PUB_SUB_URL"]

class JWT:
    DECODE_OPTIONS = {"verify_exp": True}
    SIGNING_KEY = os.environ["CORE_SECRET_KEY"]
