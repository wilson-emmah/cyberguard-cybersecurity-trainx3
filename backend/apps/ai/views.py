import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from apps.training.models import Attempt

class AIChatView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        message=str(request.data.get('message','')).strip()
        history=request.data.get('history',[])
        if not message:return Response({'detail':'Message is required.'},status=400)
        key=os.getenv('GEMINI_API_KEY')
        if not key:return Response({'detail':'Gemini AI is not configured. Add GEMINI_API_KEY to the Render environment.'},status=503)
        try:
            from google import genai
            client=genai.Client(api_key=key)
            attempts=Attempt.objects.filter(user=request.user).select_related('scenario')
            weak={}
            for a in attempts:
                x=weak.setdefault(a.scenario.scenario_type,[0,0]);x[0]+=1;x[1]+=int(a.correct)
            profile=request.user.profile
            context=f"User level {profile.level}, XP {profile.points}. Performance: {weak}."
            system=("You are CyberGuard AI Coach, a safe cybersecurity awareness tutor. "
                    "Teach defensive cybersecurity only. Never provide malware, credential theft, evasion, exploitation or attack instructions. "
                    "Explain concepts clearly, use realistic but harmless examples, and adapt to the learner. "
                    "When a question could enable harm, redirect to a safe lab or defensive explanation. "+context)
            transcript="\n".join([f"{x.get('role','user')}: {x.get('content','')}" for x in history[-8:]])
            prompt=f"{system}\n\nConversation:\n{transcript}\nuser: {message}\ncoach:"
            model=os.getenv('GEMINI_MODEL','gemini-2.5-flash-lite')
            result=client.models.generate_content(model=model,contents=prompt)
            return Response({'reply':getattr(result,'text',None) or 'I could not generate a response. Try again.'})
        except Exception as exc:
            return Response({'detail':f'AI service error: {str(exc)[:240]}'},status=502)
