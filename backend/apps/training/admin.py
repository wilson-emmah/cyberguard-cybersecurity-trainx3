from django.contrib import admin
from .models import Course,Scenario,Attempt,TrainingSession
admin.site.register([Course,Scenario,Attempt,TrainingSession])
