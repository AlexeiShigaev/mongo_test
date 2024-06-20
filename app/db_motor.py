import asyncio
import datetime
import time
import motor.motor_asyncio

from models import QueryInfo

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://mongoadmin:GhjcnjGfhjkm12@localhost:27017"
)
db = mongo_client["sampleDB"]


query_dict1 = {
    "dt_from": "2022-09-01T00:00:00",
    "dt_upto": "2022-12-31T23:59:00",
    "group_type": "month"
}

query_dict2 = {
   "dt_from": "2022-02-01T00:00:00",
   "dt_upto": "2022-02-02T00:00:00",
   "group_type": "hour"
}

query_dict3 = {
    "dt_from": "2022-10-01T00:00:00",
    "dt_upto": "2022-11-30T23:59:00",
    "group_type": "day"
}


async def test_find(query: QueryInfo):
    cursor = db.sample_collection.find(
        {"dt": {"$gte": query.dt_from, "$lte": query.dt_upto}}
    )
    for data in await cursor.to_list(None):
        print(data)


async def test_aggregation3(query: QueryInfo):
    """время выполения  0.06444549560546875"""

    # надо решить какую группировку делать
    if query.group_type == 'month':
        date_format_str = "%Y-%m-01T00:00:00"
    elif query.group_type == 'day':
        date_format_str = "%Y-%m-%dT00:00:00"
    else:  # hour
        date_format_str = "%Y-%m-%dT%H:00:00"

    """
    Если в базе нет данных за несколько дней например, в искомом периоде, 
    то и нулей в табличке не получится. И тут или лукапом сливать две таблицы 
    (вторую заранее подготовить, чтоб все строки были) или результат патчить...
    Только для этого делаю словарь предварительно заполняю его нулями.
    """
    result_data = {}
    dt = query.dt_from
    while dt <= query.dt_upto:
        result_data[dt.strftime(date_format_str)] = 0
        if query.group_type == 'month':
            dt = datetime.datetime(dt.year + int(dt.month / 12), ((dt.month % 12) + 1), 1)
        elif query.group_type == 'day':
            dt += datetime.timedelta(days=1)
        else:
            dt += datetime.timedelta(hours=1)

    # Собственно, агрегация:
    cursor = db.sample_collection.aggregate(
        [
            #  отобрать только нужный временной промежуток
            {"$match": {"dt": {"$gte": query.dt_from, "$lte": query.dt_upto}}},
            #  группирую по дате/месяцу/часу
            {"$group": {
                "_id": {"$dateToString": {"format": date_format_str, "date": "$dt"}},
                "value1": {"$sum": "$value"}
            }},
            #  далее сортировка
            {"$sort": {"_id": 1}}
        ]
    )

    data = await cursor.to_list(None)
    for el in data:
        result_data[el["_id"]] = el["value1"]

    return result_data

