from django.conf import settings
from django.db import models
from django.utils import timezone
class StaffProfile(models.Model):
 role=models.CharField(max_length=10,choices=[('ADMIN','Administrator'),('TEACHER','Teacher')],default='TEACHER')
 user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='staff_profile')
 phone=models.CharField(max_length=30,blank=True); subject=models.CharField(max_length=100,blank=True)
 def __str__(self): return f'{self.user.username} ({self.role})'
class SchoolClass(models.Model):
 name=models.CharField(max_length=80,unique=True); level=models.CharField(max_length=12,choices=[('Nursery','Nursery'),('Primary','Primary'),('Secondary','Secondary')]); teacher=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL); capacity=models.PositiveIntegerField(default=35)
 def __str__(self): return self.name
class Student(models.Model):
 admission_number=models.CharField(max_length=40,unique=True); first_name=models.CharField(max_length=80); last_name=models.CharField(max_length=80); other_names=models.CharField(max_length=80,blank=True)
 gender=models.CharField(max_length=10,choices=[('Male','Male'),('Female','Female')],blank=True); date_of_birth=models.DateField(null=True,blank=True)
 level=models.CharField(max_length=12,choices=[('Nursery','Nursery'),('Primary','Primary'),('Secondary','Secondary')]); school_class=models.ForeignKey(SchoolClass,on_delete=models.PROTECT,related_name='students')
 guardian_name=models.CharField(max_length=160,blank=True); guardian_phone=models.CharField(max_length=30,blank=True); address=models.TextField(blank=True)
 fee_due=models.DecimalField(max_digits=12,decimal_places=2,default=0); active=models.BooleanField(default=True); admission_date=models.DateField(default=timezone.localdate); created_at=models.DateTimeField(auto_now_add=True)
 @property
 def full_name(self): return ' '.join(x for x in [self.first_name,self.other_names,self.last_name] if x)
 def __str__(self): return f'{self.admission_number} - {self.full_name}'
class AttendanceRecord(models.Model):
 student=models.ForeignKey(Student,on_delete=models.CASCADE); school_class=models.ForeignKey(SchoolClass,on_delete=models.CASCADE); date=models.DateField(default=timezone.localdate)
 status=models.CharField(max_length=10,choices=[('Present','Present'),('Absent','Absent'),('Late','Late'),('Excused','Excused')],default='Present'); marked_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
 class Meta: constraints=[models.UniqueConstraint(fields=['student','date'],name='unique_daily_attendance')]
class FeePayment(models.Model):
 student=models.ForeignKey(Student,on_delete=models.PROTECT,related_name='payments'); receipt_number=models.CharField(max_length=40,unique=True); payment_date=models.DateField(default=timezone.localdate)
 amount=models.DecimalField(max_digits=12,decimal_places=2); payment_type=models.CharField(max_length=80,default='School fees'); method=models.CharField(max_length=20,choices=[('Cash','Cash'),('Bank transfer','Bank transfer'),('POS','POS'),('Other','Other')],default='Cash')
 recorded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT); reference=models.CharField(max_length=100,blank=True)
class ExamResult(models.Model):
 student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='results'); school_class=models.ForeignKey(SchoolClass,on_delete=models.PROTECT); subject=models.CharField(max_length=100); session=models.CharField(max_length=20,default='2026/2027')
 term=models.CharField(max_length=20,choices=[('First Term','First Term'),('Second Term','Second Term'),('Third Term','Third Term')],default='First Term'); score=models.PositiveSmallIntegerField(); teacher=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='taught_results'); entered_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
 class Meta: constraints=[models.UniqueConstraint(fields=['student','subject','session','term'],name='unique_term_subject_result')]
 def grade(self): return 'A' if self.score>=70 else 'B' if self.score>=60 else 'C' if self.score>=50 else 'D' if self.score>=45 else 'E' if self.score>=40 else 'F'
