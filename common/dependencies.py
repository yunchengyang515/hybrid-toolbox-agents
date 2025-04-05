from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from .config import settings

async def verify_api_key(x_api_key: str = Header(None)):
    """Verify the API key provided in the X-API-Key header."""
    if settings.API_KEY and (not x_api_key or x_api_key != settings.API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return True
