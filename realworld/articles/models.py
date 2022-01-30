from __future__ import annotations

from datetime import datetime

import markdown
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from taggit.models import Tag

User = get_user_model()


class ArticleQuerySet(models.QuerySet):
    def with_favorites(self, user: AnonymousUser | User) -> models.QuerySet:

        return self.annotate(
            num_favorites=models.Count("favorites"),
            is_favorite=models.Exists(
                get_user_model().objects.filter(
                    pk=user.id, favorites=models.OuterRef("pk")
                ),
            )
            if user.is_authenticated
            else models.Value(False, output_field=models.BooleanField()),
        )


ArticleManager = models.Manager.from_queryset(ArticleQuerySet)


class Article(models.Model):
    author: User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title: str = models.CharField(max_length=120)
    summary: str = models.TextField(blank=True)
    content: str = models.TextField(blank=True)

    created: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)

    tags: list[Tag] = TaggableManager(blank=True)

    favorites: list[User] = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="favorites"
    )

    objects = ArticleManager()

    def __str__(self) -> str:
        return self.title

    @property
    def slug(self) -> str:
        return slugify(self.title)

    def get_absolute_url(self) -> str:
        return reverse(
            "article_detail",
            kwargs={
                "article_id": self.id,
                "slug": self.slug,
            },
        )

    def as_markdown(self) -> str:
        return markdown.markdown(self.content, safe_mode="escape", extensions=["extra"])
