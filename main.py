import httpx
from fastapi import Depends, HTTPException, status,FastAPI
from fastapi.security import OAuth2PasswordBearer
AUTH_SERVICE_URL = "http://localhost:8000/token/verify"
# AUTH_SERVICE_URL = "http://localhost:8000/data/demo"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

app = FastAPI()


async def verify_token(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AUTH_SERVICE_URL, json={"token": token}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        return response.json()

@app.get("/user/current_user")
async def get_current_user(authorization: str = Depends(oauth2_scheme)):
    token = authorization
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorization token missing"
        )

    token_data = await verify_token(token)
    return token_data

@app.get("/")
async def function():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_SERVICE_URL
        )
    return response.json()
