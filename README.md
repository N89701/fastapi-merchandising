# Merchandising API

Данное приложение является API по учету партий товаров и продуктов в каждой партии.
Стек:
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- Pytest
- PostgreSQL
- Docker
- Github Actions

## Как запустить?
Клонировать репозиторий
```
git clone git@github.com:N89701/fastapi-merchandising.git
```
Запустить локально тесты (тесты запускаются на тестовой базе данных, которая создается перед тестами и удаляется сразу после)
```
pip install pytest
pytest
```
Запустить докер-оркестр с приложением и базой данных и открыть его по адресу
```
docker compose up
http://localhost:8008/docs#/
```
Приложение работает и готово навести суету в базе данных.
P.s.  .env удалено из gitignore сознательно, для более быстрого и удобного тестирования.