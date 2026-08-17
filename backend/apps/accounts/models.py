from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
 user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
 role=models.CharField(max_length=20,choices=[('user','User'),('admin','Admin')],default='user')
 points=models.PositiveIntegerField(default=0); level=models.PositiveIntegerField(default=1)
 def __str__(self): return self.user.username
