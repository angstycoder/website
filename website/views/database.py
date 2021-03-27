from redis import Redis
from passlib.apps import custom_app_context as pwd_context


class AuthenticationStore:
    def __init__(self, host: str, port: int, password: str):
        self.redis = Redis(host=host, port=port, password=password)

    def validate_hex(self, user: str, password: str):
        user_cred = self.redis.get(user)
        return pwd_context.verify(password, user_cred)

    def create_user(self, user:str, password: str):
        pass_hash = pwd_context.hash(password)
        return self.redis.set(user, pass_hash)
