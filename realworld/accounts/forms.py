from django import forms
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class UserCreationForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ["email", "name"]

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class SettingsForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ["email", "name", "bio", "image"]

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
