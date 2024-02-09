import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BatchCreate(BaseModel):
    status: bool = Field(..., alias="СтатусЗакрытия")
    assignment: str = Field(..., alias="ПредставлениеЗаданияНаСмену")
    line: str = Field(..., alias="Линия")
    shift: str = Field(..., alias="Смена")
    squad: str = Field(..., alias="Бригада")
    number: int = Field(..., alias="НомерПартии")
    date: datetime.date = Field(..., alias="ДатаПартии")
    nomenclature: str = Field(..., alias="Номенклатура")
    codekn: str = Field(..., alias="КодЕКН")
    identificator_rc: str = Field(..., alias="ИдентификаторРЦ")
    start_time: datetime.datetime = Field(..., alias="ДатаВремяНачалаСмены")
    end_time: datetime.datetime = Field(..., alias="ДатаВремяОкончанияСмены")


class BatchRead(BaseModel):
    id: int
    status: bool
    assignment: str
    line: str
    shift: str
    squad: str
    number: int
    date: datetime.date
    nomenclature: str
    codekn: str
    identificator_rc: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    closed_at: Optional[datetime.datetime]
