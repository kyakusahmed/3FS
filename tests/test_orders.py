"""Tests for API endpoints."""
import unittest
import random
import json
from app.view import app

BASE_URL = "/api/v1/orders"

class OrderTest(unittest.TestCase):
    """Order Tests."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.test_order = {"menu_id": 10, "client_id": 5, "quantity": 1, "location": "Bukoto"}

    def test_get_orders(self):
        """Test get all orders."""
        response = self.app.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data.decode('utf-8')).get('orders'), list)

    def test_post_order(self):
        """Post new order."""
        test_data = {
            "client_id": random.randint(100, 200),
            "location": "Bukoto",
            "menu_id": random.randint(300, 400),
            "quantity": 2
        }
        response = self.app.post(BASE_URL, json=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data.decode('utf-8'))['data']['location'], "Bukoto")

    def test_get_specific_order(self):
        """Test get specific order."""
        self.app.post(BASE_URL, json=self.test_order)
        response = self.app.get(BASE_URL + "/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode('utf-8')).get('order')[0]['quantity'], 1)
        self.assertEqual(json.loads(response.data.decode('utf-8')).get('order')[0]['location'], "Bukoto")
        self.assertEqual(json.loads(response.data.decode('utf-8')).get('order')[0]['status'], "pending")

    def test_get_specific_order_not_found(self):
        """Test specific order not found."""
        response = self.app.get(BASE_URL + "/98989")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data.decode('utf-8')).get('message'), "Cannot find this order")

    def test_update_specific_order(self):
        """Test update specific order."""
        status = {"status": "completed"}
        self.app.post(BASE_URL, json=self.test_order)
        response = self.app.put(BASE_URL + "/1", json=status)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode('utf-8')).get('data')[0]['status'], "completed")

    def test_update_specific_order_not_found(self):
        """Test for updating order not found."""
        status = {"status": "completed"}
        response = self.app.put(BASE_URL + "/98989", json=status)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data.decode('utf-8')).get('error'), "Unable to find this order")

    def tearDown(self):
        """Destroy variable test_order."""
        self.test_order = dict()