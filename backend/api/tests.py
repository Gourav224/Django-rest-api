from django.test import TestCase
from api.models import User, Order
from django.urls import reverse
from rest_framework import status
# Create your tests here.


class UserOrderTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username="user1", password="test")
        self.user2 = User.objects.create_user(username="user2", password="test")

        self.order1 = Order.objects.create(user=self.user1)
        self.order2 = Order.objects.create(user=self.user1)
        self.order3 = Order.objects.create(user=self.user2)
        self.order4 = Order.objects.create(user=self.user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.get(reverse("user-orders"))

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order["user"] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse("user-orders"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
