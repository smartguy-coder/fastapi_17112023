from fastapi import status


def test_root_status_code(client):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK


def test_root_content(client):
    response = client.get('/')
    assert response.json() == {'try': 'OK', 'count': 10}
