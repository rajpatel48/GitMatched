from werkzeug.test import Client
from werkzeug.testapp import test_app
import unittest
c = Client(test_app)

def test__dashboard(client):
    response = client.get("http://localhost:5000/dashboard")
    client.assertEqual(response.status_code, 200)
    client.assertIn(b'Dashboard opens', response.data)

test__dashboard(c)