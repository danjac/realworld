from __future__ import annotations

from realworld.articles.models import Article
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from .forms import CommentForm
from .models import Comment


@require_http_methods(["POST"])
@login_required
def add_comment(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(Article, pk=article_id)
    comment: Comment | None = None

    if (form := CommentForm(request.POST)).is_valid():

        comment = form.save(commit=False)
        comment.author = request.user
        comment.article = article
        comment.save()

        # reset form
        form = CommentForm()

    return TemplateResponse(
        request,
        "comments/_comment_form.html",
        {
            "article": article,
            "form": form,
            "new_comment": comment,
        },
    )


@require_http_methods(["GET", "POST"])
@login_required
def edit_comment(request: HttpRequest, comment_id: int) -> HttpResponse:

    comment = get_object_or_404(
        Comment.objects.select_related("author"),
        author=request.user,
        pk=comment_id,
    )

    if request.method == "GET":

        return TemplateResponse(
            request,
            "comments/_comment_form.html",
            {
                "comment": comment,
                "form": CommentForm(instance=comment),
            },
        )

    if (form := CommentForm(request.POST, instance=comment)).is_valid():
        comment = form.save()

        return TemplateResponse(request, "comments/_comment.html", {"comment": comment})

    return TemplateResponse(
        request,
        "comments/_comment_form.html",
        {
            "comment": comment,
            "form": form,
        },
    )


@require_http_methods(["DELETE"])
@login_required
def delete_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(
        Comment,
        author=request.user,
        pk=comment_id,
    )
    comment.delete()
    return HttpResponse()
