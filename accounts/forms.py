from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

    class Meta:
        model = User
        fields = ('email', 'password')



class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'Votre email'
        })
    )

    def confirm_login_allowed(self, user):
        """Contrôle supplémentaire si besoin."""
        if not user.is_active:
            raise forms.ValidationError(
                _("Ce compte est désactivé. Contactez l’administrateur."),
                code='inactive',
            )
