from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect
from realworld.comments.forms import CommentForm
from realworld.comments.models import Comment
from taggit.models import Tag

from .forms import ArticleForm
from .models import Article


@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:

    articles = (
        Article.objects.select_related("author")
        .with_favorites(request.user)
        .prefetch_related("tags")
        .order_by("-created")
    )

    if own_feed := request.user.is_authenticated and "own" in request.GET:
        articles = articles.filter(author=request.user)

    if tag := request.GET.get("tag"):
        articles = articles.filter(tags__name__in=[tag])

    tags = Tag.objects.all()

    return TemplateResponse(
        request,
        "articles/home.html",
        {
            "articles": articles,
            "own_feed": own_feed,
            "tags": tags,
        },
    )


@require_http_methods(["GET"])
def article_detail(request: HttpRequest, article_id: int, slug: str) -> HttpResponse:

    article = get_object_or_404(
        Article.objects.select_related("author").with_favorites(request.user),
        pk=article_id,
    )

    comments = (
        Comment.objects.filter(article=article)
        .select_related("author")
        .order_by("-created")
    )

    context = {
        "article": article,
        "comments": comments,
        "is_favorite": article.is_favorite,
        "num_favorites": article.num_favorites,
    }

    if request.user.is_authenticated:
        context.update(
            {
                "is_author": article.author == request.user,
                "comment_form": CommentForm(),
            }
        )

    return TemplateResponse(request, "articles/article.html", context)


@require_http_methods(["GET", "POST"])
@login_required
def create_article(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request,
            "articles/article_form.html",
            {"form": ArticleForm()},
        )

    if (form := ArticleForm(request.POST)).is_valid():

        article = form.save(commit=False)
        article.author = request.user
        article.save()

        # save tags
        form.save_m2m()

        return HttpResponseClientRedirect(article.get_absolute_url())

    return TemplateResponse(request, "articles/_article_form.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
def edit_article(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(Article, pk=article_id, author=request.user)

    if request.method == "GET":

        return TemplateResponse(
            request,
            "articles/article_form.html",
            {
                "form": ArticleForm(instance=article),
                "article": article,
            },
        )

    if (form := ArticleForm(request.POST, instance=article)).is_valid():
        form.save()
        return HttpResponseClientRedirect(article.get_absolute_url())

    return TemplateResponse(
        request,
        "articles/_article_form.html",
        {
            "form": form,
            "article": article,
        },
    )


@require_http_methods(["DELETE"])
@login_required
def delete_article(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(Article, pk=article_id, author=request.user)
    article.delete()
    return HttpResponseRedirect(reverse("home"))


@require_http_methods(["POST", "DELETE"])
@login_required
def favorite(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(
        Article.objects.select_related("author").exclude(author=request.user),
        pk=article_id,
    )

    is_favorite: bool

    if request.method == "DELETE":
        article.favorites.remove(request.user)
        is_favorite = False
    else:
        article.favorites.add(request.user)
        is_favorite = True

    return TemplateResponse(
        request,
        "articles/_favorite_action.html",
        {
            "article": article,
            "is_favorite": is_favorite,
            "num_favorites": article.favorites.count(),
            "is_action": True,
            "is_detail": False
            if request.htmx.target == f"favorite-{article.id}"
            else True,
        },
    )


@require_http_methods(["GET"])
def tags_autocomplete(request: HttpRequest) -> HttpResponse:

    # find the latest item in tag string

    search: str = ""

    try:
        search = request.GET["tags"].split()[-1].strip()
    except (KeyError, IndexError):
        pass

    tags = (
        Tag.objects.filter(name__istartswith=search).distinct()
        if search
        else Tag.objects.none()
    )

    return TemplateResponse(request, "articles/_tags.html", {"tags": tags})
