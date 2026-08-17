from django.contrib.auth.models import User
from django.db import models
class Badge(models.Model):
 name=models.CharField(max_length=100); description=models.TextField(); icon=models.CharField(max_length=20,default='🏆'); requirement_points=models.PositiveIntegerField(default=0)
class UserBadge(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE); badge=models.ForeignKey(Badge,on_delete=models.CASCADE); earned_at=models.DateTimeField(auto_now_add=True)
 class Meta: unique_together=('user','badge')
