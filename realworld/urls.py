from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("realworld.articles.urls")),
    path("", include("realworld.accounts.urls")),
    path("comments/", include("realworld.comments.urls")),
    path("admin/", admin.site.urls),
]
