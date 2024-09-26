from app.models import OrderStatus
from common import client, setup_test_db
from test_products import product_data

order_data = {
    "status": OrderStatus.in_process.value,
}

updated_order_data = {
    "status": OrderStatus.delivered.value,
}


def test_create_order(setup_test_db):
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == OrderStatus.in_process


def test_get_orders(setup_test_db):
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    data1 = response.json()
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    data2 = response.json()
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    data3 = response.json()

    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert data == [data1, data2, data3]


def test_get_order(setup_test_db):
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    order_id = response.json()["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == order_data["status"]


def test_update_order(setup_test_db):
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    order_id = response.json()["id"]

    response = client.patch(f"/orders/{order_id}/status", params=updated_order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == updated_order_data["status"]


def test_add_item_to_order(setup_test_db):
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    order_id = response.json()["id"]

    response = client.post("/products", json=product_data)
    assert response.status_code == 200
    product_id = response.json()["id"]

    order_item_data = {
        "order_id": order_id,
        "product_id": product_id,
        "quantity": 100
    }

    response = client.post(f"/orders/{order_id}/items", json=order_item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == order_item_data["order_id"]
    assert data["product_id"] == order_item_data["product_id"]
    assert data["quantity"] == order_item_data["quantity"]

    response = client.post(f"/orders/{order_id}/items", json=order_item_data)
    assert response.status_code == 200
    response = client.post(f"/orders/{order_id}/items", json=order_item_data)
    assert response.status_code == 400