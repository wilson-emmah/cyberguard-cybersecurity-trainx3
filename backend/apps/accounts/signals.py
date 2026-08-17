from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
@receiver(post_save,sender=User)
def profile(sender,instance,created,**kwargs):
 if created: Profile.objects.create(user=instance,role='admin' if instance.is_staff or instance.is_superuser else 'user')
