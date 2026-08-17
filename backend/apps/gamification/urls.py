from django.urls import path
from .views import LeaderboardView,BadgeView
urlpatterns=[path('leaderboard/',LeaderboardView.as_view()),path('badges/me/',BadgeView.as_view())]
