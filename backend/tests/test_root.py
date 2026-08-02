def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "app_name" in data