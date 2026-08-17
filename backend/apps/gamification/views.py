from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .models import UserBadge

class LeaderboardView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request):
        users=User.objects.select_related("profile").order_by("-profile__points","username")[:50]
        return Response([{"rank":i,"username":u.username,"points":u.profile.points,"level":u.profile.level} for i,u in enumerate(users,1)])

class BadgeView(APIView):
    def get(self,request):
        rows=UserBadge.objects.filter(user=request.user).select_related("badge")
        return Response([{"name":x.badge.name,"description":x.badge.description,"icon":x.badge.icon,"earned_at":x.earned_at} for x in rows])
