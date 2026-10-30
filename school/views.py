import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Count,Q
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Student,StaffProfile,SchoolClass,AttendanceRecord,FeePayment,ExamResult
from .forms import StudentForm,ClassForm,AttendanceForm,PaymentForm,ResultForm
from .permissions import is_admin,admin_only
def login_view(request):
 if request.user.is_authenticated: return redirect('dashboard')
 error=''
 if request.method=='POST':
  user=authenticate(request,username=request.POST.get('username',''),password=request.POST.get('password',''))
  if user and user.is_active: login(request,user); return redirect('dashboard')
  error='Username or password is incorrect.'
 return render(request,'school/login.html',{'error':error})
@login_required
def logout_view(request):
 if request.method=='POST': logout(request)
 return redirect('login')
@login_required
def dashboard(request):
 return render(request,'school/dashboard.html',{'student_count':Student.objects.filter(active=True).count(),'staff_count':StaffProfile.objects.count(),'class_count':SchoolClass.objects.count(),'fee_total':FeePayment.objects.aggregate(v=Sum('amount'))['v'] or Decimal('0'),'recent':Student.objects.select_related('school_class').order_by('-created_at')[:8],'is_admin':is_admin(request.user)})
@login_required
def students(request):
 if request.method=='POST':
  form=StudentForm(request.POST)
  if form.is_valid(): form.save(); messages.success(request,'Student saved.'); return redirect('students')
 else: form=StudentForm()
 q=request.GET.get('q','').strip()
 qs=Student.objects.select_related('school_class').order_by('last_name','first_name')
 if q: qs=qs.filter(Q(first_name__icontains=q)|Q(last_name__icontains=q)|Q(admission_number__icontains=q))
 return render(request,'school/students.html',{'students':qs,'form':form,'is_admin':is_admin(request.user)})
@login_required
@admin_only
def staff(request): return render(request,'school/staff.html',{'profiles':StaffProfile.objects.select_related('user').all(),'is_admin':True})
@login_required
def classes(request):
 if request.method=='POST':
  if not is_admin(request.user): return HttpResponseForbidden()
  form=ClassForm(request.POST)
  if form.is_valid(): form.save(); messages.success(request,'Class saved.'); return redirect('classes')
 else: form=ClassForm()
 return render(request,'school/classes.html',{'classes':SchoolClass.objects.annotate(n=Count('students')),'form':form,'is_admin':is_admin(request.user)})
@login_required
def attendance(request):
 if request.method=='POST':
  form=AttendanceForm(request.POST)
  if form.is_valid():
   obj=form.save(commit=False); obj.marked_by=request.user; obj.school_class=obj.student.school_class
   try: obj.save(); messages.success(request,'Attendance saved.')
   except Exception: messages.error(request,'Attendance for this student and date may already exist.')
   return redirect('attendance')
 else: form=AttendanceForm(initial={'date':timezone.localdate()})
 return render(request,'school/attendance.html',{'form':form,'records':AttendanceRecord.objects.select_related('student','school_class','marked_by').order_by('-date')[:100],'is_admin':is_admin(request.user)})
@login_required
@admin_only
def fees(request):
 if request.method=='POST':
  form=PaymentForm(request.POST)
  if form.is_valid():
   obj=form.save(commit=False); obj.recorded_by=request.user; obj.receipt_number='BIS-'+timezone.now().strftime('%y%m%d%H%M%S%f')[-14:]; obj.save()
   messages.success(request,'Payment recorded. Receipt: '+obj.receipt_number); return redirect('fees')
 else: form=PaymentForm()
 return render(request,'school/fees.html',{'form':form,'payments':FeePayment.objects.select_related('student')[:100],'total':FeePayment.objects.aggregate(v=Sum('amount'))['v'] or Decimal('0'),'is_admin':True})
@login_required
def results(request):
 if request.method=='POST':
  form=ResultForm(request.POST)
  if form.is_valid():
   obj=form.save(commit=False); obj.entered_by=request.user; obj.school_class=obj.student.school_class
   try: obj.save(); messages.success(request,'Result saved.')
   except Exception: messages.error(request,'A result for this subject, session and term already exists.')
   return redirect('results')
 else: form=ResultForm()
 return render(request,'school/results.html',{'form':form,'results':ExamResult.objects.select_related('student','school_class','teacher').order_by('-id')[:150],'is_admin':is_admin(request.user)})
@login_required
@admin_only
def reports(request):
 return render(request,'school/reports.html',{'student_count':Student.objects.filter(active=True).count(),'class_count':SchoolClass.objects.count(),'payment_count':FeePayment.objects.count(),'fee_total':FeePayment.objects.aggregate(v=Sum('amount'))['v'] or Decimal('0'),'result_count':ExamResult.objects.count(),'is_admin':True})
@login_required
@admin_only
def export_json(request):
 payload={'exported_at':timezone.now().isoformat(),'students':list(Student.objects.values('admission_number','first_name','last_name','level','school_class__name','guardian_name','guardian_phone','fee_due','active')),'classes':list(SchoolClass.objects.values('name','level','capacity')),'attendance':list(AttendanceRecord.objects.values('student__admission_number','date','status')),'payments':list(FeePayment.objects.values('receipt_number','student__admission_number','payment_date','amount','payment_type','method')),'results':list(ExamResult.objects.values('student__admission_number','subject','session','term','score'))}
 return JsonResponse(payload)
def manifest(request): return JsonResponse({'name':'Brightway International Schools','short_name':'Brightway','start_url':'/','display':'standalone','background_color':'#f4f7fa','theme_color':'#142f4b','icons':[]})
def service_worker(request):
 js="""const C='brightway-shell-v1';self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(['/login/'])));self.skipWaiting()});self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));self.addEventListener('fetch',e=>{if(e.request.method!=='GET'||new URL(e.request.url).origin!==location.origin)return;e.respondWith(fetch(e.request).then(r=>{if(r.ok&&e.request.mode==='navigate'){caches.open(C).then(c=>c.put(e.request,r.clone()))}return r}).catch(()=>caches.match(e.request).then(r=>r||caches.match('/login/'))))});"""
 return HttpResponse(js,content_type='application/javascript')
