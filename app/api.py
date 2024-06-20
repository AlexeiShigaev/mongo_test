from fastapi import APIRouter

from db_motor import test_aggregation3
from models import QueryInfo


router = APIRouter(tags=["api"])


@router.get("/api/get_data")
async def get_data(query: QueryInfo):
    print("get_data request: {}".format(query))
    ret = await test_aggregation3(query)
    results = {"dataset": [], "labels": []}
    for key, elem in ret.items():
        results["dataset"].append(elem)
        results["labels"].append(key)

    return results

