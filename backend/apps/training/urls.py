from django.urls import path
from .views import CourseListView,ScenarioListView,AttemptListView,SubmitScenarioView,AdminScenarioView,StartSessionView,ActiveSessionView,SaveSessionView,RiskView,AdminAnalyticsView
urlpatterns=[
 path('courses/',CourseListView.as_view()),path('scenarios/',ScenarioListView.as_view()),
 path('scenarios/<int:pk>/submit/',SubmitScenarioView.as_view()),path('attempts/me/',AttemptListView.as_view()),
 path('sessions/start/',StartSessionView.as_view()),path('sessions/active/',ActiveSessionView.as_view()),
 path('sessions/<int:pk>/save/',SaveSessionView.as_view()),path('risk/me/',RiskView.as_view()),
 path('admin/scenarios/',AdminScenarioView.as_view()),path('admin/analytics/',AdminAnalyticsView.as_view())
]