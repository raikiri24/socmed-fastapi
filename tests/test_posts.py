
not_expiring_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJpZCI6MywiZXhwIjo4ODA5MDE3ODMyOH0.bDvLWsAQAJFOQEKt7JALSmwDB2wEEITcVnSPa6pfHCQ"
test_login_user = "string"
test_login_password = "string"


def test_create_post(client):
    response = client.post("posts/", data={"title": "test", "description": "test"}, headers={
        "Authorization": f"Bearer {not_expiring_token}",
        "content-type": "application/json"
    }
    )
    assert response.status_code == 200


def test_is_array_posts(client):
    response = client.get("posts/users", headers={
        "Authorization": f"Bearer {not_expiring_token}"
    }
    )

    assert response.status_code == 200
    assert isinstance(response.json()["message"], list)
