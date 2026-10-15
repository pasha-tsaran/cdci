# Server Time API

Простой тестовый бэкенд на FastAPI. Требуется Python 3.10 или новее.

## Запуск в PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

## Запуск через Docker

Из папки проекта выполните:

```powershell
docker build -t server-time-api .
docker run --rm -p 8000:8000 server-time-api
```

API доступен по адресу http://127.0.0.1:8000/time,
Swagger — http://127.0.0.1:8000/docs. Для остановки нажмите `Ctrl+C`.
В контейнере используется его локальный часовой пояс (по умолчанию UTC).

## Запрос текущего времени

Откройте http://127.0.0.1:8000/time или выполните:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/time
```

Пример JSON-ответа:

```json
{"server_time": "2026-10-15T12:34:56.123456+03:00"}
```

Время вычисляется при каждом запросе в локальном часовом поясе сервера.
Значение возвращается в формате ISO 8601 со смещением относительно UTC.
Кэширование ответа отключено.

Интерактивная документация API: http://127.0.0.1:8000/docs.

Документация FastAPI: https://fastapi.tiangolo.com/tutorial/first-steps/.
