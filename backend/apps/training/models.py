from django.contrib.auth.models import User
from django.db import models

class Course(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    description=models.TextField()
    category=models.CharField(max_length=100)
    published=models.BooleanField(default=True)
    order=models.PositiveIntegerField(default=0)
    def __str__(self): return self.title

class Scenario(models.Model):
    title=models.CharField(max_length=200)
    scenario_type=models.CharField(max_length=30,choices=[
        ('phishing','Phishing'),('url','Suspicious URL'),('password','Password Security'),
        ('malware','Malware'),('incident','Incident Response')
    ])
    difficulty=models.PositiveSmallIntegerField(default=1)
    description=models.TextField()
    prompt=models.TextField()
    choices=models.JSONField(default=list)
    correct_choice=models.PositiveIntegerField()
    explanation=models.TextField()
    points=models.PositiveIntegerField(default=100)
    published=models.BooleanField(default=True)
    course=models.ForeignKey(Course,null=True,blank=True,on_delete=models.SET_NULL)
    def __str__(self): return self.title

class Attempt(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    scenario=models.ForeignKey(Scenario,on_delete=models.CASCADE)
    selected_choice=models.PositiveIntegerField()
    correct=models.BooleanField()
    points_awarded=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

class TrainingSession(models.Model):
    STATUS_CHOICES=[('active','Active'),('completed','Completed'),('abandoned','Abandoned')]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='training_sessions')
    course=models.ForeignKey(Course,null=True,blank=True,on_delete=models.SET_NULL,related_name='sessions')
    scenario_ids=models.JSONField(default=list)
    current_index=models.PositiveIntegerField(default=0)
    score=models.PositiveIntegerField(default=0)
    answered_ids=models.JSONField(default=list)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='active')
    started_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    class Meta:
        indexes=[models.Index(fields=['user','status']),models.Index(fields=['user','updated_at'])]
    @property
    def progress(self):
        total=len(self.scenario_ids)
        return round((len(self.answered_ids)/total)*100) if total else 0
