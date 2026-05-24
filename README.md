# Python app for Docker container test

Небольшое приложение на Python с Flask, которое поднимает HTTP-сервер для проверки, что контейнер корректно запускается.

## Что делает приложение

- Слушает порт `5000` (или значение переменной `PORT`).
- Отдаёт JSON на `GET /` и `GET /health`.
- Возвращает базовую информацию: статус, hostname контейнера, версию Python и текущее UTC-время.
- Отдаёт информацию о системе на `GET /info`.
- Считает процент на `GET /percent/<a>/<b>` (процент `a` от числа `b`).
- Считает факториал на `GET /fact/<x>`.
- Для неизвестных роутов возвращает JSON-ошибку `404`.

## Локальный запуск без Docker

```bash
pip install -r requirements.txt
python main.py
```

## Сборка Docker-образа

Выполните в директории проекта:

```bash
docker build -t python-container-test:latest .
```

## Запуск контейнера

```bash
docker run --rm -p 5000:5000 --name python-test-app python-container-test:latest
```

## Проверка работы

Откройте в браузере:

- `http://localhost:5000/`
- `http://localhost:5000/health`
- `http://localhost:5000/info`
- `http://localhost:5000/percent/20/150`
- `http://localhost:5000/fact/5`

Или через curl:

```bash
curl http://localhost:5000/health
```

## Запуск через Docker Compose (backend + frontend)

В проект добавлен фронтенд-сервис, который показывает данные Flask API и отправляет запросы к backend по внутренней сети compose.

Запуск:

```bash
docker compose up --build
```

Запуск в фоне (detached mode):

```bash
docker compose up --build -d
```

Остановка и удаление контейнеров compose:

```bash
docker compose down
```

После запуска:

- UI фронтенда: `http://localhost:8080`
- Внешний доступ к backend не требуется (запросы идут из фронтенда на `backend:5000` внутри compose через `/api/*`).

