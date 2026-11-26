# Warehouse Booking

Бэкенд для записи машин дистрибьюторов на приёмку склада. 

Организации двух типов — `company` (Астана Моторс, видит и пишет на любой склад) и
`distributor` (видит и пишет только на свои склады). Дистрибьютор записывает партию машин
одним Excel-файлом на конкретный склад и дату, в пределах фиксированного дневного лимита.

## Стек

Python 3.12, FastAPI, SQLAlchemy 2.0 (async), PostgreSQL + asyncpg, Alembic, `pyjwt`,
`openpyxl`, `httpx`, пакетный менеджер `uv`.

## Как запустить локально

Нужны: Python 3.12, [`uv`](https://docs.astral.sh/uv/), Docker (для Postgres).

```bash
# 1. Зависимости
uv sync

# 2. Конфиг — .env.example уже содержит рабочие для локального запуска значения
cp .env.example .env

# 3. Postgres в контейнере
docker compose up -d

# 4. Миграции
cd src && uv run alembic upgrade head && cd ..

# 5. Тестовые данные (организации, склады, несколько активных записей)
uv run python scripts/seed_data.py
```

Дальше нужны **два** постоянно работающих процесса, каждый в своём окне терминала:

```bash
# Основной сервис — http://localhost:8000/docs
uv run uvicorn main:app --reload --app-dir src

# Мок сервиса учёта — http://localhost:8001/docs
uv run uvicorn mock_accounting:app --port 8001 --reload
```

## Пример Excel-файла

В папке `samples/`:

| Файл | Что проверяет |
|---|---|
| `bookings_sample.xlsx` | Основной пример — одним файлом сразу все причины ответа: успешная запись, нехватка мест, неверный формат VIN, VIN не найден в учёте, дубликат VIN внутри файла, VIN уже имеет активную запись |
| `all_booked.xlsx` | Все строки успешно записываются |
| `all_rejected.xlsx` | Все строки отклонены («Нет в учёте») |
| `vin_not_first_column.xlsx` | Колонка VIN не первая, значение с пробелами по краям |
| `empty_data.xlsx` | Файл без единой строки данных (только заголовок) |
| `no_vin_column.xlsx` | Нет колонки с заголовком «VIN» — должен отклонить файл целиком |
| `too_many_rows.xlsx` | 205 строк — больше лимита в 200 |
| `exactly_200_rows.xlsx` | Ровно 200 строк — граничное значение, не должно отклоняться |

## Эндпойнты

| Метод | Путь | Описание |
|---|---|---|
| GET | `/warehouses` | Список складов, видимых организации токена |
| GET | `/warehouses/{id}/calendar?year=&month=` | Занято/лимит по каждому дню месяца |
| GET | `/warehouses/{id}/availability?date=` | Свободно N из M на конкретную дату |
| POST | `/warehouses/{id}/bookings/upload?date=` | Загрузка `.xlsx` с VIN, запись машин |
