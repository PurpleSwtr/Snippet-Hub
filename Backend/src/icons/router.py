from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi_cache.decorator import cache

from src.core.config import settings 
from src.icons.service import get_icons_names, get_icon
router = APIRouter(prefix='/icons', tags=['Icons'])

@router.get("/namelist/{pack}")
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.icons_list) 
async def list_icons(pack: str):
    print("Данные с диска")
    try:
        data = get_icons_names(pack=pack)
        if not data:
            raise NotADirectoryError
        return data
    except NotADirectoryError:
        raise HTTPException(status_code=404, detail="Pack not found")

# @router.get("/static/{pack}/{filename}")
# async def get_icon_file(pack: str, filename: str):
#     try:
#         icon_path = get_icon(pack=pack, filename=filename)
#         return FileResponse(icon_path, media_type="image/svg+xml")
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="Icon not found")
