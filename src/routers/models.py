from typing import List
from fastapi import APIRouter, HTTPException, status

from src.models.model import Model
from src.db import db

router = APIRouter()

@router.get("/")
async def all() -> List[float]:
    return list(db.predictions)

@router.post("/", status_code=status.HTTP_201_CREATED) 
async def create_predictions() -> List[float]:
    model = Model()
    predictions = model.forecast(model.model, model.test_x, 48).tolist()
    predictions =[float(f'{i:.2f}') for i in predictions]
    db.predictions = predictions
    return predictions