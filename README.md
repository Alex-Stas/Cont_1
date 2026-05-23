# Python app for Docker container test

Небольшое приложение на Python с Flask, которое поднимает HTTP-сервер для проверки, что контейнер корректно запускается.

## Что делает приложение

- Слушает порт `8000` (или значение переменной `PORT`).
- Отдаёт JSON на `GET /` и `GET /health`.
- Возвращает базовую информацию: статус, hostname контейнера, версию Python и текущее UTC-время.
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
docker run --rm -p 8000:8000 --name python-test-app python-container-test:latest
```

## Проверка работы

Откройте в браузере:

- `http://localhost:8000/`
- `http://localhost:8000/health`

Или через curl:

```bash
curl http://localhost:8000/health
```

