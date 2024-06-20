# mongo_test
MongoDB aggregation data

## Подготовка
Поскольку общение происходит через бота telegram,<br>
в main.py нужно bot_token. Все детали знает BotFather.<br>
Использован telethon. Ему нужно api_id и api_hash. Сделать можно в API Development tools 
 [здесь](https://my.telegram.org/auth)

## запуск
MongoDB разворачивается в докере
`docker compose up --build`
Коллекция стартовых данных наполнится автоматически. Подсмотреть можно через mongo-express [http://127.0.0.1:8081](http://127.0.0.1:8081)
(Он тоже разворачивается)

дальше все просто
```
cd app
poetry install
python main.py
```
