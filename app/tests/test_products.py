from common import client, setup_test_db


product_data = {
    "name": "Test Product",
    "description": "Test Description",
    "price": 100.23,
    "stock": 200
}

updated_product_data = {
    "name": "Updated Product",
    "description": "Updated Description",
    "price": 150.34,
    "stock": 140
}


def test_create_product(setup_test_db):
    response = client.post("/products", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == str(product_data["price"])
    assert data["stock"] == product_data["stock"]


def test_get_products(setup_test_db):
    create_response = client.post(f"/products", json=product_data)
    assert create_response.status_code == 200
    data1 = create_response.json()
    create_response = client.post(f"/products", json=updated_product_data)
    assert create_response.status_code == 200
    data2 = create_response.json()
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == [data1, data2]


def test_get_product(setup_test_db):
    create_response = client.post(f"/products", json=product_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == str(product_data["price"])
    assert data["stock"] == product_data["stock"]


def test_update_product(setup_test_db):
    create_response = client.post("/products", json=product_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    update_response = client.put(f"/products/{product_id}", json=updated_product_data)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == updated_product_data["name"]
    assert data["description"] == updated_product_data["description"]
    assert data["price"] == str(updated_product_data["price"])
    assert data["stock"] == updated_product_data["stock"]


def test_delete_product(setup_test_db):
    create_response = client.post("/products", json=product_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"products/{product_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["id"] == product_id

    get_response = client.get(f"products/{product_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Товар не найден"}