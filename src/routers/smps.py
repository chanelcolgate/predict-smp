from typing import List, Any
from fastapi import APIRouter, HTTPException, status

from src.models.smp import SMP
from src.db import db

router = APIRouter()

@router.get("/{k}")
async def get_scores(k: int) -> List[Any]:
    scores_key = db.scores[-k:]
    scores_key.sort(key = lambda tup: tup[0][1])
    return scores_key[-1:]

@router.get("/power/{id}")
async def get_power(id: int) -> List[float]:
    predictions = db.predictions
    smp = SMP(expectedPrice = predictions, sheetName = ['29-09'], n = 24)
    return smp.get_index(key = id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_scores() -> List[Any]:
    predictions = db.predictions
    smp = SMP(expectedPrice = predictions, sheetName = ['29-09'], n = 24)
    scores = smp.scores
    db.scores = scores
    return db.scores[-1:]