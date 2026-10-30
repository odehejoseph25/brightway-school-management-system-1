from django import forms
from .models import Student,SchoolClass,AttendanceRecord,FeePayment,ExamResult
class StudentForm(forms.ModelForm):
 class Meta:
  model=Student; fields=['admission_number','first_name','last_name','other_names','gender','date_of_birth','level','school_class','guardian_name','guardian_phone','address','fee_due','admission_date','active']
  widgets={'date_of_birth':forms.DateInput(attrs={'type':'date'}),'admission_date':forms.DateInput(attrs={'type':'date'}),'address':forms.Textarea(attrs={'rows':2})}
class ClassForm(forms.ModelForm):
 class Meta: model=SchoolClass; fields=['name','level','teacher','capacity']
class AttendanceForm(forms.ModelForm):
 class Meta:
  model=AttendanceRecord; fields=['student','date','status']
  widgets={'date':forms.DateInput(attrs={'type':'date'})}
class PaymentForm(forms.ModelForm):
 class Meta:
  model=FeePayment; fields=['student','payment_date','amount','payment_type','method','reference']
  widgets={'payment_date':forms.DateInput(attrs={'type':'date'})}
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw); self.fields['amount'].widget.attrs.update({'min':'0.01','step':'0.01'})
class ResultForm(forms.ModelForm):
 class Meta:
  model=ExamResult; fields=['student','subject','session','term','score','teacher']
 def clean_score(self):
  v=self.cleaned_data['score']
  if v>100: raise forms.ValidationError('Score cannot exceed 100.')
  return v
