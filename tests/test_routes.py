import json

import config

connex_app = config.connex_app
connex_app.add_api('swagger.yml')
connex_app = connex_app.app

client = connex_app.test_client()


def test_director_read_all():
    url = '/api/director'

    response = client.get(url)
    data = json.loads(response.get_data())
    assert isinstance(data, list) is True
    assert response.status_code == 200

def test_movie_read_all():
    url = '/api/movies'

    response = client.get(url)
    data = json.loads(response.get_data())
    assert isinstance(data, list) is True
    assert response.status_code == 200

def test_director_byId():
    url = '/api/director/6671'

    response = client.get(url)
    data = json.loads(response.get_data())
    assert isinstance(data, dict) is True
    assert response.status_code == 200

def test_movie_byId():
    url = '/api/director/6671/movies/47728'

    response = client.get(url)
    data = json.loads(response.get_data())
    assert isinstance(data, dict) is True
    assert response.status_code == 200