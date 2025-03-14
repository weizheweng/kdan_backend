# app/routers/pharmacies.py
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session
from typing import Dict, List, Literal, Optional
from datetime import time
from app.database import get_db
from app.models import Pharmacy, Mask, DayOfWeekEnum
from app.schemas import MaskBase, Pharmacy as PharmacySchema, Mask as MaskSchema
from app.utils.time_helper import is_open_now


router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])

@router.get("/all_pharmacies", response_model=List[PharmacySchema])
def list_all_pharmacies(db: Session = Depends(get_db)):
    """
    撈全部藥局 (即 pharmacies 表內所有資料)
    """
    return db.query(Pharmacy).all()

@router.get("/open", response_model=List[PharmacySchema])
def get_open_pharmacies(day_of_week: DayOfWeekEnum, time_str: Optional[str], db: Session = Depends(get_db)):
    """
    List all pharmacies open at a specific time and on a day of week if requested.
    e.g. GET /pharmacies/open?day_of_week=Thur&time_str=14:00
    """
    query = db.query(Pharmacy)
    pharmacies = query.all()

    # 轉換 time_str -> time
    hour_min = time_str.split(":")
    check_time = time(int(hour_min[0]), int(hour_min[1]) if len(hour_min) > 1 else 0)

    result = []
    for ph in pharmacies:
        ohs = ph.opening_hours
        is_open = False
        for oh in ohs:
            if oh.day_of_week.value == day_of_week:
                if is_open_now(oh.open_time, oh.close_time, check_time):
                    is_open = True
                    break
        if is_open:
            result.append(ph)
    return result

@router.get("/{pharmacy_id}/masks", response_model=List[MaskSchema])
def list_masks_of_pharmacy(
    pharmacy_id: int = Path(..., description="The ID of the pharmacy"),
    sort_by: Literal["name", "price"] = Query("name", description="Sort masks by 'name' or 'price'."),
    sort_order: Literal["asc", "desc"] = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending."),
    db: Session = Depends(get_db)
):
    """
    List all masks sold by a given pharmacy, sorted by mask name or price.
    e.g. GET /pharmacies/5/masks?sort_by=price&sort_order=desc
    """
    q = db.query(Mask).filter(Mask.pharmacy_id == pharmacy_id)
    
    # 根據 sort_by 來決定排序欄位
    sort_column = Mask.name if sort_by == "name" else Mask.price
    
    # 根據 sort_order 決定升序 (asc) 或 降序 (desc)
    q = q.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))
    
    return q.all()

@router.get("/filter", response_model=List[PharmacySchema])
def filter_pharmacies_mask_count(
    count_op: Literal["gt", "lt"],
    count_value: int,
    price_min: float,
    price_max: float,
    db: Session = Depends(get_db)
):
    """
    List all pharmacies with more or less than x mask products within a price range.
    e.g. GET /pharmacies/filter?count_op=gt&count_val=3&price_min=10&price_max=50
    """
    # 先找出在 price_min~price_max 之間的 masks
    subq = db.query(Mask.pharmacy_id).filter(Mask.price.between(price_min, price_max))

    # group by pharmacy_id, 並計算符合該區間的口罩數量
    subq_count = (db.query(Mask.pharmacy_id, func.count(Mask.id).label("cnt"))
                  .filter(Mask.price.between(price_min, price_max))
                  .group_by(Mask.pharmacy_id)
                  ).subquery()

    # 再與 pharmacies join
    query = db.query(Pharmacy).join(subq_count, subq_count.c.pharmacy_id == Pharmacy.id)

    # 篩選 count_op
    if count_op == "gt":
        query = query.filter(subq_count.c.cnt > count_value)
    else:
        query = query.filter(subq_count.c.cnt < count_value)

    return query.all()

@router.get("/all_masks", response_model=Dict[str, List[MaskBase]])
def list_all_masks(db: Session = Depends(get_db)):
    """
    撈全部藥局的口罩 (即 masks 表內所有資料)
    """
    query = (
        select(
            Mask.id,
            Mask.name.label('mask_name'),
            Mask.pharmacy_id,
            Mask.price,
            Pharmacy.name.label('pharmacy_name'),
        )
        .join(Pharmacy)
    )
    result = db.execute(query).all()
    
    # 將結果整理成以藥局為 key 的字典
    grouped_masks = {}
    for row in result:
        data = dict(row._mapping)
        pharmacy_name = data.pop('pharmacy_name')
        if pharmacy_name not in grouped_masks:
            grouped_masks[pharmacy_name] = []
        grouped_masks[pharmacy_name].append(data)
    
    return grouped_masks