"""tests app"""
from blogy import create_app


class TestApp:
    """test general requests"""

    def test_config(self):
        """check if we are in testing mode"""
        assert create_app({'TESTING': True}).testing

    def test_hello(self, client):
        """test /status endpoint"""
        response = client.get('/status')
        assert response.status_code == 200
        assert response.json == {'status': 'OK'}
