from typing import List, Any
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import FileResponse

from src.models.offer import Offer
from src.db import db
from os import path

router = APIRouter()

@router.get("/{nameExcel}")
async def get_offer(nameExcel: str = 'Bảng chào giá'):
    root_directory = path.dirname(path.dirname(__file__))
    excel_path = path.join(root_directory, "../data", f"{nameExcel}.xlsx")
    if path.exists(excel_path):
        return FileResponse(excel_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{nameExcel}.xlsx")
    return {"error" : "File not found!"}
    

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_offer(
    nameExcel: str = 'Bảng chào giá',
    date: str = '29/09/2021',
    power: List[float] = [0.0],
    Pmin: float = Query(11.0, ge=11.0),
    CSCB: float = Query(13.0, le=22.0),
    ceilPrice: float = Query(1503.5, le=1503.5),
    # smp: List[float] = [0.0]
) -> bool:
    offer = Offer(Pmin=Pmin, CSCB=CSCB, smp=db.predictions, power=power, mucGiaTran = ceilPrice)
    # offer = Offer(Pmin=Pmin, CSCB=CSCB, smp=smp, power=power, mucGiaTran = ceilPrice)
    offer.createOffer(nameExcel=nameExcel, date=date)
    return True