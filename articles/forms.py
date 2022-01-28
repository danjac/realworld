from __future__ import annotations

from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "summary", "content", "tags"]
        widgets = {"summary": forms.TextInput()}
