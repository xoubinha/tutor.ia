from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("", response_class=JSONResponse)
def health_check():
    return {"status": "OK"}