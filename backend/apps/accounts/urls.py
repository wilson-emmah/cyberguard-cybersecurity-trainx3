from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterView,MeView,AdminUsersView,AdminStatsView
urlpatterns=[path('auth/register/',RegisterView.as_view()),path('auth/token/',TokenObtainPairView.as_view()),path('auth/token/refresh/',TokenRefreshView.as_view()),path('auth/me/',MeView.as_view()),path('admin/users/',AdminUsersView.as_view()),path('admin/stats/',AdminStatsView.as_view())]
