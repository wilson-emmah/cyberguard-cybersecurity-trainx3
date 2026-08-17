from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency('auth.User')]
    operations=[
      migrations.CreateModel(name='Course',fields=[
        ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
        ('title',models.CharField(max_length=200)),('slug',models.SlugField(unique=True)),('description',models.TextField()),
        ('category',models.CharField(max_length=100)),('published',models.BooleanField(default=True)),('order',models.PositiveIntegerField(default=0))]),
      migrations.CreateModel(name='Scenario',fields=[
        ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=200)),
        ('scenario_type',models.CharField(choices=[('phishing','Phishing'),('url','Suspicious URL'),('password','Password Security'),('malware','Malware'),('incident','Incident Response')],max_length=30)),
        ('difficulty',models.PositiveSmallIntegerField(default=1)),('description',models.TextField()),('prompt',models.TextField()),('choices',models.JSONField(default=list)),
        ('correct_choice',models.PositiveIntegerField()),('explanation',models.TextField()),('points',models.PositiveIntegerField(default=100)),('published',models.BooleanField(default=True)),
        ('course',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to='training.course'))]),
      migrations.CreateModel(name='Attempt',fields=[
        ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('selected_choice',models.PositiveIntegerField()),
        ('correct',models.BooleanField()),('points_awarded',models.PositiveIntegerField(default=0)),('created_at',models.DateTimeField(auto_now_add=True)),
        ('scenario',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to='training.scenario')),('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to='auth.user'))]),
      migrations.CreateModel(name='TrainingSession',fields=[
        ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('scenario_ids',models.JSONField(default=list)),
        ('current_index',models.PositiveIntegerField(default=0)),('score',models.PositiveIntegerField(default=0)),('answered_ids',models.JSONField(default=list)),
        ('status',models.CharField(choices=[('active','Active'),('completed','Completed'),('abandoned','Abandoned')],default='active',max_length=20)),
        ('started_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('completed_at',models.DateTimeField(blank=True,null=True)),
        ('course',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='sessions',to='training.course')),
        ('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='training_sessions',to='auth.user'))]),
      migrations.AddIndex(model_name='trainingsession',index=models.Index(fields=['user','status'],name='training_tr_user_id_6f3d0c_idx')),
      migrations.AddIndex(model_name='trainingsession',index=models.Index(fields=['user','updated_at'],name='training_tr_user_id_9d7db8_idx')),
    ]
