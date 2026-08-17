from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
 initial=True
 dependencies=[migrations.swappable_dependency('auth.User')]
 operations=[
  migrations.CreateModel(name='Badge',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=100)),('description',models.TextField()),('icon',models.CharField(default='🏆',max_length=20)),('requirement_points',models.PositiveIntegerField(default=0))]),
  migrations.CreateModel(name='UserBadge',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('earned_at',models.DateTimeField(auto_now_add=True)),('badge',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to='gamification.badge')),('user',models.ForeignKey(on_delete=django.db.models.CASCADE,to='auth.user'))]),
  migrations.AlterUniqueTogether(name='userbadge',unique_together={('user','badge')})]
