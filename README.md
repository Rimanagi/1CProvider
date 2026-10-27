# 1C Provider

`1C Provider` — промежуточный API-сервис между внешними системами и 1С.
Внешний сервис обращается к Provider по HTTP, а Provider получает справочные
данные из 1С и передаёт в неё выявленные дефекты.

Сервис не является хранилищем данных 1С: его задача — валидировать входящие
данные, привести ответы 1С к предсказуемому API-контракту и изолировать
внешнего клиента от особенностей 1С.

## Возможности

- Проверка работоспособности: `GET /api/v1/health/`.
- Получение из 1С типовых дефектов, причин дефектов и объектов ремонта.
- Приём дефекта от внешней системы, валидация его структуры и передача в 1С.
- Преобразование CSV-выгрузки объектов ремонта в JSON-ответ API.

Интерактивная документация доступна после запуска по адресу
`http://127.0.0.1:52010/docs`.

## Конфигурация

Настройки читаются из файла `.env` в корне проекта. Создай его по примеру:

```dotenv
APP__HOST=0.0.0.0
APP__PORT=52010

LOG__LOG_LEVEL=INFO
MODE=DEV

ONEC__BASE_URL=https://one-c.example.local/1C_TOIR/hs/MobileCircumvention/
ONEC__LOGIN=your_login
ONEC__PASSWORD=your_password
ONEC__TIMEOUT_SEC=20
```

Файл `.env` содержит секреты и уже исключён из Git. Не добавляй в него
настоящие учётные данные в README, коммиты или логи.

## Локальный запуск с uv

Требуется Python 3.11 или новее и установленный [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m src.main
```

Для разработки с автоматической перезагрузкой:

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 52010 --reload
```

## Локальный запуск без uv

`requirements.txt` содержит зафиксированные production-зависимости, поэтому
для запуска `uv` не обязателен.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
python -m src.main
```

На рабочей машине Python должен быть собран с поддержкой SSL: без неё `pip` не
сможет скачивать зависимости по HTTPS.

## Тесты и проверки

```bash
uv run pytest
uv run ruff check .
uv run pyright
```

## Docker

Собрать образ без прокси:

```bash
docker build -t 1c-provider:0.1.0 .
```

Запустить контейнер:

```bash
docker run --rm --env-file .env -p 52010:52010 1c-provider:0.1.0
```

На корпоративной сети прокси передаётся в момент сборки через аргументы, а во
время запуска — через переменные окружения. Адреса, логины и пароли прокси не
добавляй в Dockerfile или в Git.

```bash
docker build \
  --build-arg HTTP_PROXY=http://proxy.example.local:8080 \
  --build-arg HTTPS_PROXY=http://proxy.example.local:8080 \
  --build-arg NO_PROXY=localhost,127.0.0.1,one-c.example.local \
  -t 1c-provider:0.1.0 .

docker run --rm --env-file .env -p 52010:52010 \
  -e HTTP_PROXY=http://proxy.example.local:8080 \
  -e HTTPS_PROXY=http://proxy.example.local:8080 \
  -e NO_PROXY=localhost,127.0.0.1,one-c.example.local \
  1c-provider:0.1.0
```

Добавь внутренний адрес 1С в `NO_PROXY`, если к нему нужно обращаться напрямую.
`httpx` использует стандартные proxy-переменные окружения по умолчанию.

## Используемые технологии

| Технология | Назначение |
| --- | --- |
| FastAPI | HTTP API и OpenAPI/Swagger-документация. |
| Pydantic / pydantic-settings | Валидация запросов, ответов и настроек из `.env`. |
| HTTPX | Асинхронные запросы к HTTP-сервисам 1С. |
| Dishka | Контейнер зависимостей и управление жизненным циклом HTTP-клиента. |
| Structlog | Структурированное логирование. |
| Tenacity | Основа для будущих повторных попыток временно неуспешных запросов. |
| Pytest / pytest-asyncio | Тестирование асинхронного кода. |
| Ruff | Линтер и проверка стиля. |
| Pyright | Статическая проверка типов. |
| Docker | Воспроизводимый запуск сервиса. |

## Структура проекта

```text
src/
├── main.py                 # точка входа
└── app/
    ├── api/                # HTTP-роуты
    ├── clients/            # клиент для HTTP API 1С
    ├── core/               # конфигурация и логирование
    ├── schema/             # Pydantic-модели API
    ├── services/           # прикладные сценарии
    ├── factory.py          # создание FastAPI-приложения
    └── providers.py        # провайдеры Dishka
tests/
├── integration/
└── unit/
```
