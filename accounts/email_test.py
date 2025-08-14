from django.core.mail import send_mail

def test_email():
    try:
        send_mail(
            subject='Test Email Django',
            message='Ceci est un email de test envoyé depuis Django.',
            from_email='mabroukchafai64@gmail.com',  # Même que EMAIL_HOST_USER
            recipient_list=['chafaimabrouk218@gmail.com'],  # Envoi vers toi-même pour tester
            fail_silently=False,
        )
        print("✅ Email envoyé avec succès.")
    except Exception as e:
        print("❌ Erreur lors de l’envoi :", e)
