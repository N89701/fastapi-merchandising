from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app.main import app
from app.models import Base

# Setup the TestClient
client = TestClient(app)

# Setup the in-memory SQLite database for testing
DATABASE_TEST_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_TEST_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_batch():
    response = client.post(
        "/batches/", json=[
            {
                "СтатусЗакрытия": False,
                "ПредставлениеЗаданияНаСмену": "Задание на тестовую смену",
                "Линия": "Тестовая",
                "Смена": "1",
                "Бригада": "Бригада тестировщиков",
                "НомерПартии": 11111,
                "ДатаПартии": "2024-02-10",
                "Номенклатура": "QA is my life",
                "КодЕКН": "11111",
                "ИдентификаторРЦ": "QA",
                "ДатаВремяНачалаСмены": "2024-01-30T20:00:00+05:00",
                "ДатаВремяОкончанияСмены": "2024-01-31T08:00:00+05:00"
            },
            {
                "СтатусЗакрытия": False,
                "ПредставлениеЗаданияНаСмену": "Задание на тестовую смену2",
                "Линия": "Тестовая2",
                "Смена": "2",
                "Бригада": "Бригада тестировщиков2",
                "НомерПартии": 22222,
                "ДатаПартии": "2024-02-11",
                "Номенклатура": "QA is my life2",
                "КодЕКН": "22222",
                "ИдентификаторРЦ": "QA2",
                "ДатаВремяНачалаСмены": "2024-01-31T20:00:00+05:00",
                "ДатаВремяОкончанияСмены": "2024-02-01T08:00:00+05:00"
            },
        ]
    )
    assert response.status_code == 201
    data = response.json()
    assert data[0]['НомерПартии'] == 11111
    assert data[0]['СтатусЗакрытия'] is False
    assert len(data) == 2


def test_list_batch():
    response = client.get("/batches/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['date'] == "2024-02-10"


def test_list_limit_offset_search():
    response = client.get("/batches/?number=22222&limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['date'] == "2024-02-11"


def test_retrieve_batch():
    response = client.get("/batches/1/")
    assert response.status_code == 200
    assert response.json()['squad'] == "Бригада тестировщиков"


def test_update_batch():
    response = client.patch("/batches/1", json={
        "identificator_rc": "This field is updated",
        "status": True
    })
    assert response.status_code == 200
    assert response.json()["identificator_rc"] == "This field is updated"
    assert response.json()["closed_at"] is not None


def test_create_product():
    response = client.post(
        "/products/", json=[
            {
                "УникальныйКодПродукта": "Fastapi",
                "НомерПартии": 11111,
                "ДатаПартии": "2024-02-10"
            },
            {
                "УникальныйКодПродукта": "Postgres",
                "НомерПартии": 22222,
                "ДатаПартии": "2024-02-11"
            },
            {
                "УникальныйКодПродукта": "Starlette",
                "НомерПартии": 11111,
                "ДатаПартии": "6519-01-31"
            },
            {
                "УникальныйКодПродукта": "SQLAlchemy",
                "НомерПартии": 86093,
                "ДатаПартии": "2024-02-10"
            }
        ]
    )
    assert response.status_code == 201
    data = response.json()
    assert data[0]["batch_number"] == 11111
    assert data[1]["code"] == "Postgres"
    assert len(data) == 2  # loaded 4, but one of these has unexist date and
    # another has unexist batch_number


def test_product_attach_to_batch():
    response = client.get("/batches/1/")
    assert response.status_code == 200
    assert response.json()["products"][0]["code"] == "Fastapi"


def test_aggregation():
    response = client.patch("/products/", json={
            "id": 1,
            "code": "Unexist product"
        }
    )
    assert response.json()["detail"]=='Product not found.'
    response = client.patch("/products/", json={
            "id": 999,
            "code": "Fastapi"
        }
    )
    assert response.json()["detail"]=='Unique code is attached to another batch'
    response = client.patch("/products/", json={
            "id": 1,
            "code": "Fastapi"
        }
    )
    assert response.json()["is_aggregated"] is True
    assert response.json()["aggregated_at"] is not None
    response = client.patch("/products/", json={
            "id": 1,
            "code": "Fastapi"
        }
    )
    assert response.json()["detail"][:27]=='Unique code already used at'    


def setup() -> None:
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    Base.metadata.drop_all(bind=engine)
