from rest_framework.permissions import BasePermission
class IsAdminUser(BasePermission):
 def has_permission(self,request,view):
  return bool(request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser or getattr(getattr(request.user,'profile',None),'role','')=='admin'))
