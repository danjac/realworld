from django.contrib.auth import login as auth_login
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import UserCreationForm


@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request, "registration/register.html", {"form": UserCreationForm()}
        )

    if (form := UserCreationForm(request.POST)).is_valid():
        user = form.save()
        auth_login(request, user)

        return HttpResponseRedirect(reverse("home"))

    return TemplateResponse(request, "registration/register.html", {"form": form})
