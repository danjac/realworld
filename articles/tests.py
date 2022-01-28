import http

from django.test import TestCase
from django.urls import reverse_lazy


class TestIndexView(TestCase):
    url = reverse_lazy("articles:index")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
