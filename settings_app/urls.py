from django.urls import path
from . import views

app_name = "settings"

urlpatterns = [
    path("", views.settings_home, name="home"),  # Page principale des paramètres
    path("profile/", views.profile_settings, name="profile"),
    path("notifications/", views.notification_settings, name="notifications"),
]
