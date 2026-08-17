from django.contrib.auth.models import User
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer,UserSerializer
from .permissions import IsAdminUser
class RegisterView(generics.CreateAPIView): queryset=User.objects.all(); serializer_class=RegisterSerializer; permission_classes=[permissions.AllowAny]
class MeView(APIView):
 def get(self,request): return Response(UserSerializer(request.user).data)
class AdminUsersView(APIView):
 permission_classes=[IsAdminUser]
 def get(self,request): return Response(UserSerializer(User.objects.select_related('profile').order_by('-date_joined'),many=True).data)
class AdminStatsView(APIView):
 permission_classes=[IsAdminUser]
 def get(self,request):
  from apps.training.models import Scenario,Attempt
  return Response({'users':User.objects.count(),'scenarios':Scenario.objects.count(),'attempts':Attempt.objects.count()})
