from django.contrib import admin
from django.urls import path
from school import views
urlpatterns=[path('admin/',admin.site.urls),path('login/',views.login_view,name='login'),path('logout/',views.logout_view,name='logout'),path('',views.dashboard,name='dashboard'),path('students/',views.students,name='students'),path('staff/',views.staff,name='staff'),path('classes/',views.classes,name='classes'),path('attendance/',views.attendance,name='attendance'),path('fees/',views.fees,name='fees'),path('results/',views.results,name='results'),path('reports/',views.reports,name='reports'),path('api/export/',views.export_json,name='export_json'),path('manifest.webmanifest',views.manifest,name='manifest'),path('service-worker.js',views.service_worker,name='service_worker')]
