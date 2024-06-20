import asyncio
import json

import uvicorn as uvicorn
from fastapi import FastAPI
from telethon import TelegramClient, events

from api import router as api_router

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'
bot_token = '12345:0123456789abcdef0123456789abcdef'
from db_motor import query_dict3, query_dict1, query_dict2, test_aggregation3
from models import QueryInfo


async def bot_event_handler(event):
    print("new event: {}".format(event.message.message))
    if event.message.message == "/start":
        await event.respond('Привет')
        await event.respond(str(query_dict1))
        await event.respond(str(query_dict2))
        await event.respond(str(query_dict3))
        return
    # предположим, сделали запрос. проверим
    try:
        query_obj = QueryInfo(**json.loads(event.message.message.replace("\'", "\"")))
        test_ret = await test_aggregation3(query_obj)
        results = {"dataset": [], "labels": []}
        for key, elem in test_ret.items():
            results["dataset"].append(elem)
            results["labels"].append(key)
        await event.respond(str(results))
    except Exception as e:
        print(e)
        await event.reply('Понимаю например так:')
        await event.respond(str(query_dict1))


async def on_start_up() -> None:
    loop = asyncio.get_event_loop()
    bot = await TelegramClient('bot', api_id, api_hash, loop=loop).start(bot_token=bot_token)
    bot.add_event_handler(bot_event_handler, events.NewMessage)
    await bot.start()
    print("Application starts")


async def on_shutdown() -> None:
    ...


def app_loader():
    app = FastAPI(
        on_startup=[on_start_up], on_shutdown=[on_shutdown]
    )
    app.include_router(api_router)
    return app


if __name__ == "__main__":
    uvicorn.run(
        'main:app_loader',
        host='0.0.0.0',
        port=8088,
        workers=3,  # flag is ignored when reloading is enabled.
        reload=True
    )
