from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from src.snippets.enums import CategoryType
from src.snippets.schemas import OptionCreate, OptionPrompt, OptionRead, OptionResponse
from src.core.dependencies import get_db

from src.core.config import settings

router = APIRouter(prefix='/options', tags=['Options'])