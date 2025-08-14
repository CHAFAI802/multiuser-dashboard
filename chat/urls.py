from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_home, name="home"),
    path("<str:room_name>/", views.chat_room, name="room"),
]
