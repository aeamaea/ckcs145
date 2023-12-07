import json

# NOTE: always begin test methods with a prefix
# like test_ etc. ::aeam

def test_index_pass(app,client):
    del app     # what is this doing?
    res = client.get('/')
    assert res.status_code == 200
    expected = {'data':'Hello Python!!!'}

    assert expected == json.loads(res.get_data(as_text=True))


def test_get_route_fail(app, client):
    del app
    res = client.get('/nonsense')
    assert res.status_code == 404

def test_post_pass(app, client):
    mock_request_data = {'request_id':100, 'payload':'Sample Message'}

    del app
    url = '/post/test'
    res = client.post(url, data=json.dumps(mock_request_data))

    assert res.status_code == 200
    expected = 'Ok'
    assert expected == res.get_data(as_text=True)
