from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("articles.urls")),
    path("", include("accounts.urls")),
    path("admin/", admin.site.urls),
]
