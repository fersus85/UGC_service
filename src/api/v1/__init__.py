from fastapi.routing import APIRouter

from api.v1.bookmarks import router as bookmarks_router
from api.v1.scores import router as scores_router

router = APIRouter()
router.include_router(scores_router)
router.include_router(bookmarks_router)
