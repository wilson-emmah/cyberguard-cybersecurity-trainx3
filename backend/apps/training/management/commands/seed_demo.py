from django.core.management.base import BaseCommand
from apps.training.models import Course,Scenario
from apps.gamification.models import Badge
from django.utils.text import slugify
class Command(BaseCommand):
    help='Seed CyberGuard demo courses, scenarios and badges'
    def handle(self,*args,**kwargs):
        courses=[
          ('Cybersecurity Fundamentals','Core defensive security awareness.','fundamentals'),
          ('Phishing Awareness','Recognize social engineering and suspicious messages.','phishing'),
          ('Safe Browsing & Passwords','Build safer authentication and browsing habits.','defense'),
          ('Incident Response','Practice decisions during a simulated cyber incident.','simulation')]
        for title,desc,cat in courses:
            c,_=Course.objects.get_or_create(slug=slugify(title),defaults={'title':title,'description':desc,'category':cat})
        c=Course.objects.get(slug='phishing-awareness')
        data=[
          ('Spot the phishing email','phishing',1,'A message says your account will be closed in 10 minutes and asks you to verify through a shortened link. What should you do?',['Click quickly','Verify through the official website/app instead of the message','Reply with your password','Forward it to friends'],1,'Urgency and embedded links are common phishing signals. Use a trusted route to verify.'),
          ('Inspect a suspicious URL','url',1,'Which signal is most useful when checking a login link?',['The page has a padlock icon','The exact domain matches the legitimate organization','The email says it is urgent','The button is blue'],1,'The registered domain is more informative than branding or urgency.'),
          ('Password decision','password',1,'Which approach is strongest for important accounts?',['Reuse one long password everywhere','Use a unique password with a password manager and MFA','Share passwords with a colleague','Store passwords in a public document'],1,'Unique credentials, a password manager, and MFA reduce account takeover risk.'),
          ('Malware investigation','malware',2,'An unknown process runs from a temporary user directory and makes unexpected network connections. What is the safest first response?',['Ignore it','Investigate, collect evidence and isolate the host','Delete random system files','Disable the entire internet'],1,'Preserve evidence and contain the affected host while investigating.')]
        for title,typ,diff,prompt,choices,correct,ex in data:
            Scenario.objects.get_or_create(title=title,defaults={'scenario_type':typ,'difficulty':diff,'description':'Interactive defensive cybersecurity scenario.','prompt':prompt,'choices':choices,'correct_choice':correct,'explanation':ex,'points':100,'course':c})
        for name,desc,pts,icon in [('First Defender','Earn your first 100 XP.',100,'🛡️'),('Phishing Hunter','Earn 300 XP.',300,'🎣'),('Cyber Defender','Earn 500 XP.',500,'🏆')]:
            Badge.objects.get_or_create(name=name,defaults={'description':desc,'requirement_points':pts,'icon':icon})
        self.stdout.write(self.style.SUCCESS('CyberGuard demo data is ready.'))
