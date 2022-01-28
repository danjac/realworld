import http

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from .models import Article

User = get_user_model()


class TestHomeView(TestCase):
    url = reverse_lazy("home")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)


class TestArticleDetailView(TestCase):
    password = "testpass"

    def setUp(self):

        self.author = User(
            email="tester@gmail.com",
            name="tester",
        )
        self.author.set_password(self.password)
        self.author.save()

        self.article = Article.objects.create(
            title="test",
            summary="test",
            content="test",
            author=self.author,
        )

        self.url = self.article.get_absolute_url()

    def test_get_is_anonymous(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response.context["article"], self.article)
        self.assertFalse(response.context["is_author"])

    def test_get_is_author(self):
        self.client.login(email=self.author.email, password=self.password)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response.context["article"], self.article)
        self.assertTrue(response.context["is_author"])
