from __future__ import annotations

from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from realworld.articles.models import Article

User = get_user_model()


class Comment(models.Model):

    article: Article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author: User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content: str = models.TextField()

    created: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)
