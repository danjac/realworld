from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse


def index(request: HttpRequest) -> HttpResponse:
    return TemplateResponse(request, "articles/index.html")
