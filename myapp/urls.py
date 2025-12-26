"""
URL configuration for Buspass360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('passengernew/', views.passengernew, name='passengernew'),
    path('passenger/', views.passenger, name='passenger'),
    path('passenger_form/', views.passenger_form, name='passenger_form'),
    path('payment_gateway/', views.payment_gateway, name='payment_gateway'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('generate_pdf/<int:uid>/', views.generate_pdf, name='generate_pdf'),
    path('admin/', admin.site.urls),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('services', views.services, name='services'),
    path('header', views.header, name='header'),
    path('haircut', views.haircut, name='haircut'),
    path('student', views.student, name='student'),
    path('cstudent', views.cstudent, name='cstudent'),
    path('bridal', views.bridal, name='bridal'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('changepass', views.changepass, name='changepass'),
    path('fpass', views.fpass, name='fpass'),
    path('otp', views.otp, name='otp'),
    path('newpass', views.newpass, name='newpass'),
    path('profile', views.profile, name='profile'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('clgstudentform/', views.clgstudentform, name='clgstudentform'),     
    path('clgstudentform1/', views.clgstudentform1, name='clgstudentform1'),  
    path('clgstudentnew/', views.clgstudentnew, name='clgstudentnew'),  
    path('clgstudentpayment/<int:id>/', views.clgstudentpayment, name='clgstudentpayment'),
    path('clgstudentreceipt/<int:id>/', views.clgstudentreceipt, name='clgstudentreceipt'),
    path('studentform/', views.student_form_view, name='studentform'),
    path('studentform1/', views.student_form_view, name='studentform1'),
    path('studentform/success/<int:student_id>/', views.student_success_view, name='student_success'),
    path('studentform/pdf/<int:student_id>/', views.generate_student_pdf, name='student_pdf'),
    path('studentnew/', views.studentnew, name='studentnew'),



]