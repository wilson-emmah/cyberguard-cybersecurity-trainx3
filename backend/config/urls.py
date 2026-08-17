from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse
def healthz(request): return JsonResponse({'status':'ok'})
urlpatterns=[path('admin/',admin.site.urls),path('healthz/',healthz),path('api/',include('apps.accounts.urls')),path('api/',include('apps.training.urls')),path('api/',include('apps.gamification.urls')),path('api/',include('apps.ai.urls'))]
