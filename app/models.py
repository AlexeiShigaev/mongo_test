from pydantic import BaseModel, model_validator
import datetime
from typing import Literal
from typing_extensions import Self


class QueryInfo(BaseModel):
    """
    Входящий запрос может быть полной чушью. Pydantic при валидации выбросит исключение,
    Если все хорошо, получаем :
    dt_from: дата/время начала промежутка для отбора
    dt_upto: дата/время окончания промежутка отбора
    group_type: тип группировки - по месяцам, дням, часам.
    """
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: Literal['month', 'day', 'hour']

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.dt_from > self.dt_upto:
            raise ValueError("dt_from > dt_upto")
        return self

