from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_product_create():
    product = {"id": 200, "name": "shirt01", "price": 25000}

    response = client.post("/product/create", json=product)

    assert response.status_code == 200
    assert response.json() == product


def test_product_get():
    response = client.get("/product/get/100")

    assert response.status_code == 200
    assert response.json() == {
        "id": 100,
        "name": "크록스",
        "price": 30000,
    }


def test_product_get_all():
    response = client.get("/product/getall")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 100, "name": "pants01", "price": 20000},
        {"id": 101, "name": "pants01", "price": 30000},
        {"id": 102, "name": "pants01", "price": 40000},
    ]


def test_product_get_rejects_non_integer_id():
    response = client.get("/product/get/not-a-number")

    assert response.status_code == 422
