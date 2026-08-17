from rest_framework import serializers
from .models import Course,Scenario,Attempt
class CourseSerializer(serializers.ModelSerializer):
 class Meta: model=Course; fields='__all__'
class ScenarioSerializer(serializers.ModelSerializer):
 class Meta: model=Scenario; fields=['id','title','scenario_type','difficulty','description','prompt','choices','points','course']
class AttemptSerializer(serializers.ModelSerializer):
 scenario_title=serializers.CharField(source='scenario.title',read_only=True)
 scenario_type=serializers.CharField(source='scenario.scenario_type',read_only=True)
 class Meta: model=Attempt; fields=['id','scenario','scenario_title','scenario_type','selected_choice','correct','points_awarded','created_at']
