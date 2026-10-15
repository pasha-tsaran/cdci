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

## Запрос текущей даты

Все эндпоинты используют метод `GET` и возвращают JSON:

| Эндпоинт | Пример ответа | Описание |
| --- | --- | --- |
| `/date` | `{"server_date": "2026-10-15"}` | Полная дата в формате `YYYY-MM-DD` |
| `/date/year` | `{"year": 2026}` | Год |
| `/date/month` | `{"month": 10}` | Номер месяца (1–12) |
| `/date/day` | `{"day": 15}` | День месяца (1–31) |

```powershell
Invoke-RestMethod http://127.0.0.1:8000/date
```

Дата вычисляется при каждом запросе в локальном часовом поясе сервера.
Кэширование ответов отключено. В Docker по умолчанию используется UTC.
После изменения кода пересоберите образ и перезапустите контейнер.

## CI/CD: GitHub Actions → GHCR → сервер

Workflow находится в `.github/workflows/deploy.yml` и состоит из двух джоб:

1. `build_and_push` собирает Docker-образ и публикует его в
   `ghcr.io/<owner>/<repository>:<commit-sha>`. Имя приводится к нижнему регистру.
2. `deploy` после успешной публикации подключается к серверу по SSH,
   скачивает образ по digest, заменяет контейнер `server-time-api`
   и проверяет ответ `/time` внутри контейнера.

Workflow запускается при push в `main` или вручную через вкладку Actions.
Развёртывание разрешено только для `main`. Если основная ветка называется иначе,
измените `branches` и условие `if` у джобы `deploy`.

В GitHub откройте **Settings → Secrets and variables → Actions → New repository secret**:

| Секрет | Значение |
| --- | --- |
| `SSH_HOST` | IP-адрес или домен сервера |
| `SSH_USER` | Пользователь для SSH |
| `SSH_KEY` | Полное содержимое приватного SSH-ключа; публичный ключ должен быть в `authorized_keys` на сервере |
| `SSH_PORT` | Порт SSH; необязателен, по умолчанию `22` |
| `SSH_FINGERPRINT` | Отпечаток публичного ключа сервера в формате `SHA256:...` |
| `GHCR_USERNAME` | GitHub-логин владельца токена для скачивания образа |
| `GHCR_TOKEN` | Personal access token **classic** с правом `read:packages` и доступом к пакету |

`GITHUB_TOKEN` для публикации GitHub выдаёт автоматически: создавать такой секрет
вручную не нужно. Workflow запрашивает `packages: write` только в джобе сборки.
Для существующего пакета нужно разрешить этому репозиторию запись в него;
учётная запись `GHCR_USERNAME` должна иметь право читать пакет.
Если организация требует SSO, авторизуйте `GHCR_TOKEN` для этой организации.

Отпечаток получите через доверенную консоль сервера:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
```

Скопируйте в `SSH_FINGERPRINT` значение, начинающееся с `SHA256:`.
Если SSH-ключ зашифрован, добавьте секрет `SSH_PASSPHRASE` и параметр
`passphrase: ${{ secrets.SSH_PASSPHRASE }}` в `with` SSH-шага.

Пример рассчитан на Linux-сервер с архитектурой `amd64` и установленным Docker.
Пользователь `SSH_USER` должен выполнять Docker-команды без `sudo` и запроса пароля.
Для ARM-сервера измените `platforms` на `linux/arm64` и настройте QEMU для сборки
на стандартном GitHub runner.
Порт `8000` должен быть свободен и доступен для клиентов.
После развёртывания API доступен по адресу `http://<SSH_HOST>:8000/time`.

При замене контейнера будет короткий простой. При неудачной проверке джоба
завершится с ошибкой; автоматический откат в этом простом примере не настроен.
Вход в GHCR на сервере использует временную папку, которая удаляется после SSH-скрипта.

Документация: [публикация Docker-образов в GitHub Actions](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images),
[аутентификация в GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry),
[SSH action](https://github.com/appleboy/ssh-action).

Интерактивная документация API: http://127.0.0.1:8000/docs.

Документация FastAPI: https://fastapi.tiangolo.com/tutorial/first-steps/.
