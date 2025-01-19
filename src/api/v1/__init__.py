from fastapi.routing import APIRouter

from api.v1.scores import router as scores_router

router = APIRouter()
router.include_router(scores_router)
