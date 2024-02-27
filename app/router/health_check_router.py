from fastapi import APIRouter


__prefix = "/health"
router = APIRouter(prefix=__prefix)

@router.get("/")
async def health_check():
    return {"text": "server is up!"}
