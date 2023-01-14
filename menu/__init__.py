from fastapi import APIRouter

from .endpoints import router as v1_router

router = APIRouter()
router.include_router(v1_router)