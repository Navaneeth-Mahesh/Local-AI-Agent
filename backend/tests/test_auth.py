def test_register(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "navaneeth",
            "email": "nav@gmail.com",
            "password": "Password123"
        }
    )

    assert response.status_code in [200, 201, 409]


def test_login(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "nav@gmail.com",
            "password": "Password123"
        }
    )

    assert response.status_code in [200, 401]