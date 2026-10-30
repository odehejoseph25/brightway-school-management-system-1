from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from .models import StaffProfile
def is_admin(user):
 if user.is_superuser: return True
 try: return user.staff_profile.role=='ADMIN'
 except StaffProfile.DoesNotExist: return False
def admin_only(view):
 @wraps(view)
 def wrapped(request,*args,**kwargs):
  if not is_admin(request.user):
   messages.error(request,'Administrator access is required.')
   return redirect('dashboard')
  return view(request,*args,**kwargs)
 return wrapped
