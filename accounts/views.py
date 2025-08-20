from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.conf import settings 
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm

User = get_user_model()

# Connexion
def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard:home')
    return render(request, 'accounts/login.html', {'form': form})

# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Votre email a été confirmé avec succès. Vous pouvez vous connecter.")
        return render(request, "accounts/email_verified.html")
    else:
        messages.error(request, "Le lien de vérification est invalide ou a expiré.")
        return render(request, "accounts/verification_failed.html")


def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verification_link = request.build_absolute_uri(
        reverse('accounts:verify-email', kwargs={'uidb64': uid, 'token': token})
    )

    subject = "Vérifiez votre adresse email"
    message = f"Bonjour {user.first_name},\n\n"
    message += "Merci de vous être inscrit. Cliquez sur le lien ci-dessous pour activer votre compte :\n"
    message += f"{verification_link}\n\n"
    message += "Si vous n’avez pas créé de compte, ignorez cet email."

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


# Inscription avec envoi lien de vérification
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # l’utilisateur doit confirmer par email
            user.save()   
            email = form.cleaned_data.get('email')
            
            send_verification_email(user,request)
            return render(request,"accounts/verification_sent_email.html"),{"email":user.email}

            messages.success(request, "Compte créé. Vérifiez votre email pour l'activer.")
            return redirect(f'/registeration/email-verification/?email={email}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})





# Réinitialisation mot de passe - demande
def password_reset_request(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            from_email='mabroukchafai64@gmail.com',  # tu peux définir ton email d’expédition
            email_template_name='registeration/password_reset_email.html'
        )
        messages.success(request, 'Si cet email existe, un lien de réinitialisation a été envoyé.')
        return redirect('accounts:login')
    return render(request, 'registration/password_reset_email.html', {'form': form})

# Password reset done
def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

# Password reset confirm
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        form = SetPasswordForm(user, request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            messages.success(request, 'Votre mot de passe a été réinitialisé.')
            return redirect('accounts:password_reset_complete')
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Le lien de réinitialisation est invalide ou expiré.')
        return redirect('accounts:password_reset')

# Password reset complete
def password_reset_complete(request):
    return render(request, 'registeration/password_reset_complete.html')

