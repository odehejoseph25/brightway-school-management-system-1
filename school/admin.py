from django.contrib import admin
from .models import StaffProfile,SchoolClass,Student,AttendanceRecord,FeePayment,ExamResult
@admin.register(StaffProfile)
class StaffAdmin(admin.ModelAdmin): list_display=('user','role','phone','subject'); list_filter=('role',)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin): list_display=('admission_number','last_name','first_name','school_class','level','active'); list_filter=('level','school_class','active'); search_fields=('admission_number','first_name','last_name','guardian_phone')
admin.site.register(SchoolClass)
admin.site.register(AttendanceRecord)
admin.site.register(FeePayment)
admin.site.register(ExamResult)
