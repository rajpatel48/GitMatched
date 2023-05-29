from werkzeug.test import Client
from werkzeug.testapp import test_app
import unittest
c = Client(test_app)

def test_profile(client):
    response = client.get("http://localhost:5000/user/salar")
    client.assertEqual(response.status_code, 200)
    client.assertIn(b'Profile page opens', response.data)

test_profile(c)