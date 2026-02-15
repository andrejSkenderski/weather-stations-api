import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from models.dtos.requests import LoginRequest


class JwtAuthenticator:

    def __init__(
            self,
            secret_key: str,
            valid_username: str,
            valid_password: str,
            algorithm: str,
            access_token_expire_minutes: int,
    ):
        self._secret_key = secret_key
        self._valid_username = valid_username
        self._valid_password = valid_password
        self._algorithm = algorithm
        self._access_token_expire_minutes = access_token_expire_minutes
        self._blacklisted_tokens: set[str] = set()

    def authenticate_user(self, request: LoginRequest) -> dict:
        if request.username != self._valid_username or request.password != self._valid_password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = self._create_access_token(request.username)
        return {"access_token": access_token, "token_type": "bearer"}

    def logout(self, token: str) -> dict:
        self._blacklisted_tokens.add(token)
        return {"message": "Logged out successfully"}

    def verify_token(self, token: str) -> dict:
        if token in self._blacklisted_tokens:
            raise HTTPException(status_code=401, detail="Token has been revoked")
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def _create_access_token(self, username: str) -> str:
        expires = datetime.now(timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        payload = {
            "sub": username,
            "exp": expires,
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
