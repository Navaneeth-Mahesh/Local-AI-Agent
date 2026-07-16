def test_get_current_user(client):

    response = client.get("/users/me")

    assert response.status_code in [
        200,
        401,
    ]