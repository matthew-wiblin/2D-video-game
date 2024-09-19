from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("retrieve_leaderboard", views.retrieve_leaderboard, name="retrieve_leaderboard"),
    path("create_user", views.create_user, name="create_user"),
    path("get_user_data", views.get_user_data, name="get_user_data"),
    path("sendscore", views.sendscore, name="sendscore")
]
