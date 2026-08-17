from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
 initial=True
 dependencies=[migrations.swappable_dependency('auth.User')]
 operations=[migrations.CreateModel(name='Profile',fields=[
  ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
  ('role',models.CharField(choices=[('user','User'),('admin','Admin')],default='user',max_length=20)),
  ('points',models.PositiveIntegerField(default=0)),('level',models.PositiveIntegerField(default=1)),
  ('user',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name='profile',to='auth.user'))])]
