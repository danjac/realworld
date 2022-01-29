from articles.models import Article
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect

from .forms import SettingsForm, UserCreationForm

User = get_user_model()


@require_http_methods(["GET"])
def profile(request: HttpRequest, user_id: int) -> HttpResponse:

    profile = get_object_or_404(User, pk=user_id)

    articles = (
        Article.objects.select_related("author")
        .filter(author=profile)
        .with_favorites(request.user)
        .prefetch_related("tags")
        .order_by("-created")
    )

    if favorites := "favorites" in request.GET:
        articles = articles.filter(num_favorites__gt=0)

    return TemplateResponse(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "articles": articles,
            "favorites": favorites,
            "is_following": profile.followers.filter(pk=request.user.id).exists(),
        },
    )


@require_http_methods(["GET", "POST"])
@login_required
def settings(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request,
            "accounts/settings.html",
            {"form": SettingsForm(instance=request.user)},
        )

    if (form := SettingsForm(request.POST, instance=request.user)).is_valid():
        form.save()
        return HttpResponseClientRedirect(request.user.get_absolute_url())

    return TemplateResponse(request, "accounts/_settings.html", {"form": form})


@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request, "registration/register.html", {"form": UserCreationForm()}
        )

    if (form := UserCreationForm(request.POST)).is_valid():
        user = form.save()
        auth_login(request, user)

        return HttpResponseClientRedirect(reverse("home"))

    return TemplateResponse(request, "registration/_register.html", {"form": form})


@require_http_methods(["POST", "DELETE"])
@login_required
def follow(request: HttpRequest, user_id: int) -> HttpResponse:

    user = get_object_or_404(User.objects.exclude(pk=request.user.id), pk=user_id)

    is_following: bool

    if request.method == "DELETE":
        user.followers.remove(request.user)
        is_following = False
    else:
        user.followers.add(request.user)
        is_following = True

    return TemplateResponse(
        request,
        "accounts/_follow_action.html",
        {
            "followed": user,
            "is_following": is_following,
            "is_action": True,
        },
    )
