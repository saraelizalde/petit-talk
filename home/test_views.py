from django.test import TestCase, Client
from django.urls import reverse


class HomeViewsBasicTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view_status_code_and_template(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_contact_view_status_code_and_template(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/contact.html")

    def test_robots_txt_view_status_code_and_content_type(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
