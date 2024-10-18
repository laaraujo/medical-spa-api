def test__pass(client, user):
    client.force_authenticate(user)
    r = client.get("/auth/users/")
    assert r.status_code == 200
