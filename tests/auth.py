from werkzeug.test import Client
from werkzeug.testapp import test_app
import unittest
c = Client(test_app)

def test_signup(client):
    response = client.post("http://localhost:5000/api/signup", headers={"email": "test@test.com", "password": "test123"})
    client.assertEqual(response.status_code, 200)
    client.assertIn(b'You have successfully signed up', response.data)

test_signup(c)

def test_login(client):
    response = client.post("http://localhost:5000/api/token", headers={"email": "test@test.com", "password": "test123"})
    client.assertEqual(response.status_code, 200)
    client.assertIn(b'You have successfully logged in', response.data)

test_login(c)