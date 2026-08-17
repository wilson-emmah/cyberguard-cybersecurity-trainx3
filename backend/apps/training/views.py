import os
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Scenario, Attempt, TrainingSession
from .serializers import CourseSerializer, ScenarioSerializer, AttemptSerializer
from apps.accounts.permissions import IsAdminUser

class CourseListView(generics.ListAPIView):
    queryset=Course.objects.filter(published=True).order_by("order")
    serializer_class=CourseSerializer
    permission_classes=[permissions.AllowAny]

class ScenarioListView(generics.ListAPIView):
    serializer_class=ScenarioSerializer
    def get_queryset(self):
        return Scenario.objects.filter(published=True).order_by("difficulty","id")

class AttemptListView(generics.ListAPIView):
    serializer_class=AttemptSerializer
    def get_queryset(self):
        return Attempt.objects.filter(user=self.request.user).select_related("scenario").order_by("-created_at")

class SubmitScenarioView(APIView):
    def post(self, request, pk):
        try: scenario=Scenario.objects.get(pk=pk,published=True)
        except Scenario.DoesNotExist: return Response({"detail":"Scenario not found."},status=404)
        try: choice=int(request.data.get("choice"))
        except (TypeError,ValueError): return Response({"detail":"A valid choice is required."},status=400)
        correct=choice==scenario.correct_choice
        points=scenario.points if correct else 0
        Attempt.objects.create(user=request.user,scenario=scenario,selected_choice=choice,correct=correct,points_awarded=points)
        profile=request.user.profile
        if correct:
            profile.points += points
            profile.level=max(1,profile.points//500+1)
            profile.save()
            from apps.gamification.models import Badge,UserBadge
            for badge in Badge.objects.filter(requirement_points__lte=profile.points):
                UserBadge.objects.get_or_create(user=request.user,badge=badge)
        return Response({"correct":correct,"points_awarded":points,"total_points":profile.points,"level":profile.level,"explanation":scenario.explanation})

class StartSessionView(APIView):
    def post(self, request):
        existing=TrainingSession.objects.filter(user=request.user,status='active').order_by('-updated_at').first()
        if existing and not request.data.get('restart'):
            return Response(self._data(existing))
        ids=list(Scenario.objects.filter(published=True).order_by('difficulty','id').values_list('id',flat=True))
        course_id=request.data.get('course_id')
        if course_id:
            ids=list(Scenario.objects.filter(published=True,course_id=course_id).order_by('difficulty','id').values_list('id',flat=True))
        if not ids: return Response({"detail":"No published scenarios are available."},status=400)
        if request.data.get('restart') and existing:
            existing.status='abandoned'; existing.save(update_fields=['status','updated_at'])
        s=TrainingSession.objects.create(user=request.user,course_id=course_id or None,scenario_ids=ids)
        return Response(self._data(s),status=201)
    def _data(self,s):
        current_id=s.scenario_ids[s.current_index] if s.scenario_ids and s.current_index<len(s.scenario_ids) else None
        scenario=Scenario.objects.filter(id=current_id,published=True).first() if current_id else None
        return {"id":s.id,"course_id":s.course_id,"status":s.status,"progress":s.progress,"score":s.score,
                "current_index":s.current_index,"total":len(s.scenario_ids),"current_scenario":ScenarioSerializer(scenario).data if scenario else None,
                "updated_at":s.updated_at}

class ActiveSessionView(APIView):
    def get(self,request):
        s=TrainingSession.objects.filter(user=request.user,status='active').order_by('-updated_at').first()
        return Response(StartSessionView()._data(s) if s else None)

class SaveSessionView(APIView):
    def post(self,request,pk):
        s=TrainingSession.objects.filter(pk=pk,user=request.user,status='active').first()
        if not s:return Response({"detail":"Active session not found."},status=404)
        if 'score' in request.data:
            try:s.score=max(0,int(request.data['score']))
            except:pass
        if 'answered_id' in request.data:
            try: sid=int(request.data['answered_id'])
            except:return Response({"detail":"Invalid scenario id."},status=400)
            if sid in s.scenario_ids and sid not in s.answered_ids:s.answered_ids.append(sid)
        if 'current_index' in request.data:
            try:s.current_index=max(0,min(int(request.data['current_index']),len(s.scenario_ids)))
            except:pass
        if s.current_index>=len(s.scenario_ids):
            s.status='completed';s.completed_at=timezone.now()
        s.save()
        return Response(StartSessionView()._data(s))

class RiskView(APIView):
    def get(self,request):
        attempts=list(Attempt.objects.filter(user=request.user).select_related('scenario'))
        categories={}
        for a in attempts:
            row=categories.setdefault(a.scenario.scenario_type,{'total':0,'correct':0,'points':0})
            row['total']+=1;row['correct']+=int(a.correct);row['points']+=a.points_awarded
        scores={k:round(v['correct']/v['total']*100) if v['total'] else 0 for k,v in categories.items()}
        overall=round(sum(a.correct for a in attempts)/len(attempts)*100) if attempts else 0
        weakest=min(scores,key=scores.get) if scores else None
        return Response({"overall":overall,"categories":scores,"weakest_area":weakest,
                         "recommendation":f"Complete more {weakest.replace('_',' ')} training." if weakest else "Start a simulation to build your security profile."})

class AdminAnalyticsView(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        from django.db.models import Q
        users=User.objects.select_related('profile')
        attempts=Attempt.objects.select_related('scenario')
        by_type={}
        for a in attempts:
            x=by_type.setdefault(a.scenario.scenario_type,[0,0]);x[0]+=1;x[1]+=int(a.correct)
        weaknesses=[{"type":k,"score":round(v[1]/v[0]*100) if v[0] else 0,"attempts":v[0]} for k,v in by_type.items()]
        weaknesses.sort(key=lambda x:x['score'])
        return Response({"users":users.count(),"attempts":attempts.count(),"courses":Course.objects.filter(published=True).count(),
                         "completed_sessions":TrainingSession.objects.filter(status='completed').count(),
                         "average_score":round(attempts.aggregate(v=Avg('points_awarded'))['v'] or 0),
                         "weaknesses":weaknesses,"high_risk_users":list(
                             users.order_by('profile__points').values('username','profile__points','profile__level')[:10])})

class AdminScenarioView(generics.ListCreateAPIView):
    queryset=Scenario.objects.all()
    serializer_class=ScenarioSerializer
    permission_classes=[IsAdminUser]
