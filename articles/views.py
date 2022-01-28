from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse


def home(request: HttpRequest) -> HttpResponse:
    return TemplateResponse(request, "articles/home.html")
