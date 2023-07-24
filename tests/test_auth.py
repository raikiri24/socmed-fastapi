
def test_return_token(client):
    response = client.post("/auth/token", data={"username": "string", "password": "string"},
                           headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
