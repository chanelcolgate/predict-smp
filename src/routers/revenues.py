from typing import List, Any, Dict
from fastapi import APIRouter, HTTPException, status, Query, Path
from fastapi.responses import FileResponse

from src.models.revenue import Revenue
from src.db import db
from os import path

router = APIRouter()

@router.get("/{nameExcel}")
async def get_revenue_excel(nameExcel: str = 'Bảng dự kiến doanh thu'):
    root_directory = path.dirname(path.dirname(__file__))
    excel_path = path.join(root_directory, "../data", f"{nameExcel}.xlsx")
    if path.exists(excel_path):
        return FileResponse(excel_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{nameExcel}.xlsx")
    return {"error" : "File not found!"}

@router.post("/report")
async def create_revenue_report(
    priceContract: float = Query(917.22),
    expectedOutput: List[float] = [0.0],
    priceCan: List[float] = [0.0],
    outputContract: List[float] = [0.0],
    Pmin: float = Query(11.0, ge=11.0),
    CSCB: float = Query(13.0, le=22.0),
    ceilPrice: float = Query(1503.5, le=1503.5)
) -> Dict[str, float]:
    data = {
        'Chu kỳ': [i for i in range(1, 49)],
        'Sản lượng dự kiến phát': expectedOutput,
        'Giá biên tham chiếu cho bản chào giá dự kiến': db.predictions,
        'Giá CAN': priceCan,
        'Sản lượng hợp đồng (Qc)': outputContract
    }
    r = Revenue(
        priceContract = priceContract,
        data = data,
        Pmin = Pmin,
        CSCB = CSCB,
        ceilPrice = ceilPrice
    )
    # print(r.getRevenue())
    return r.getRevenue()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_revenue(
    nameExcel: str = 'Bảng dự kiến doanh thu',
    date: str = 'Ngày 29/9/2021',
    priceContract: float = Query(917.22),
    expectedOutput: List[float] = [0.0],
    priceCan: List[float] = [0.0],
    outputContract: List[float] = [0.0],
    Pmin: float = Query(11.0, ge=11.0),
    CSCB: float = Query(13.0, le=22.0),
    ceilPrice: float = Query(1503.5, le=1503.5)
) -> bool:
    data = {
        'Chu kỳ': [i for i in range(1, 49)],
        'Sản lượng dự kiến phát': expectedOutput,
        'Giá biên tham chiếu cho bản chào giá dự kiến': db.predictions,
        'Giá CAN': priceCan,
        'Sản lượng hợp đồng (Qc)': outputContract
    }
    r = Revenue(
        priceContract = priceContract,
        data = data,
        Pmin = Pmin,
        CSCB = CSCB,
        ceilPrice = ceilPrice
    )
    r.createRevenue(nameExcel = nameExcel, date = date)
    return True
    