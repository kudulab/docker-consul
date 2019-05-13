import requests as r

def test_api():
    with r.get('http://localhost:9500/v1/agent/members') as res:
        assert res.status_code == 200