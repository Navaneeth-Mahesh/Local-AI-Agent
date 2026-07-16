def test_get_settings(client):

    response = client.get("/settings")

    assert response.status_code in [
        200,
        401,
    ]