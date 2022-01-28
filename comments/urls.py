from django.urls import path

from . import views

urlpatterns = [
    path(
        "add/<int:article_id>/",
        views.add_comment,
        name="add_comment",
    ),
    path(
        "edit/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment",
    ),
    path(
        "delete/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment",
    ),
]
