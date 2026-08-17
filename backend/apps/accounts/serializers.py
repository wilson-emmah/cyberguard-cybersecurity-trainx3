from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
class RegisterSerializer(serializers.ModelSerializer):
 password=serializers.CharField(write_only=True,min_length=8)
 class Meta: model=User; fields=['username','email','password']
 def validate_email(self,v):
  if User.objects.filter(email__iexact=v).exists(): raise serializers.ValidationError('An account with this email already exists.')
  return v.lower()
 def validate_password(self,v): validate_password(v); return v
 def create(self,d): return User.objects.create_user(**d)
class UserSerializer(serializers.ModelSerializer):
 points=serializers.IntegerField(source='profile.points',read_only=True); level=serializers.IntegerField(source='profile.level',read_only=True); role=serializers.CharField(source='profile.role',read_only=True)
 class Meta: model=User; fields=['id','username','email','points','level','role']
