from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sendscore", views.check_and_update_high_score, name="check_and_update_high_score"),
    path("retrieve_leaderboard", views.retrieve_leaderboard, name="retrieve_leaderboard")
]
