from django.test import TestCase
from django.contrib.auth.models import User
from order.models import Order


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pass123"
        )

    def test_create_order(self):
        order = Order.objects.create(student=self.user)
        self.assertEqual(order.student.username, "testuser")
        self.assertFalse(order.paid)

    def test_order_str(self):
        order = Order.objects.create(student=self.user)
        text = str(order)
        self.assertIn("Order", text)
        self.assertIn("testuser", text)

    def test_get_or_create_basket(self):
        basket1 = Order.get_or_create_basket(self.user)
        basket2 = Order.get_or_create_basket(self.user)
        self.assertEqual(basket1.id, basket2.id)

    def test_calculate_methods_do_not_crash(self):
        order = Order.objects.create(student=self.user)
        self.assertIsNotNone(order.calculate_subtotal())
        self.assertIsNotNone(order.calculate_total())
