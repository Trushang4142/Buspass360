from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from . models import *
import random
import requests
from .models import Appointment
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password, check_password

from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from io import BytesIO
from django.conf import settings


#from django.core.mail import send_mail
#from django.conf import settings


def index(request):
    return render(request,'index.html')

# Create your views here.

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def passenger_form(request):
    return render(request, 'passenger_form.html')

def services(request):
    return render(request,'services.html')

def header(request):
    return render(request,'header.html')

def haircut(request):
    return render(request,'haircut.html')

def student(request):
    return render(request,'student.html')

def cstudent(request):
    return render(request,'cstudent.html')

def bridal(request):
    return render(request,'bridal.html')



def studentnew(request):
    return render(request,'studentnew.html')


def payment_gateway(request):
    return render(request,'payment_gateway.html')

def clgstudentnew(request):
    return render(request,'clgstudentnew.html')

def clgstudentform(request):
    return render(request,'clgstudentform.html')




def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            return render(request, 'signup.html', {'msg': "Email already exists!"})
        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
                hashed_password = make_password(request.POST['password'])
                user = User.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    password=hashed_password
                )
                # ✅ Save basic session (optional)
                request.session['email'] = user.email
                request.session['name'] = user.name
                request.session['is_logged_in'] = False  # Not logged in yet

                return render(request, 'login.html', {'msg': "Signup Successfully! Please login to continue."})
            else:
                return render(request, 'signup.html', {'msg': "Password & Confirm Password Do Not Match!"})
    return render(request, 'signup.html')



def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if check_password(request.POST['password'], user.password):
                request.session['email'] = user.email
                request.session['name'] = user.name
                request.session['is_logged_in'] = True  # ✅ Logged in flag
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg': "Password Does Not Match!!"})
        except User.DoesNotExist:
            return render(request, 'login.html', {'msg': "Email is not Registered!!"})
    return render(request, 'login.html')



def logout(request):
    request.session.flush()  # clears all session data
    return redirect('login')


def changepass(request):
        user = User.objects.get(email=request.session['email'])
        if request.method == "POST":

            if user.password == request.POST['opassword']:
                if request.POST['npassword'] == request.POST['cnpassword']:
                    user.password = request.POST['npassword']
                    user.save()
                    msg = "Password Updated Successfully!!"
                    return redirect('logout')
                    
                else:
                    msg = "New Password & confirm new password does not match!!"
                    return render(request, 'changepass.html', {'msg': msg})
                   
            else:
                msg = "Old Password does not match!!"
                return render(request, 'changepass.html', {'msg': msg})
               
        else:
           return render(request,'changepass.html')

def fpass(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(mobile=request.POST['mobile'])
            mobile = request.POST['mobile']
            otp = random.randint(1001,9999)
            import requests

            url = "https://www.fast2sms.com/dev/bulkV2"

            querystring = {"authorization":"mCoZfjo0Qsv9YHj7o7yMZsJaxfOeRZf8NySm5AUdH6TyGjxGE6JZoCo1SkJ6","variables_values":str(otp),"route":"otp","numbers":mobile}

            headers = {
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            request.session['mobile'] = user.mobile
            request.session['otp'] = otp
            return render(request,'otp.html')
        except User.DoesNotExist:
            msg = "Mobile Number does not exist!!"
            return render(request,'fpass.html',{'msg':msg})
        except Exception as e:
            print(e)
            msg = "An error occured.please try again!"
            return render(request,'fpass.html',{'msg':msg})
    else:
        return render(request,'fpass.html')

def otp(request):
    try:
        otp = int(request.session['otp'])
        uotp = int(request.POST['uotp'])
        print(otp)
        print(uotp)
        if otp == uotp:
            del request.session['otp']
            return render(request,'newpass.html')
        else:
            msg = "Invalid OTP!"
            return render(request,'otp.html',{'msg':msg})
    except Exception as e:
        print(e) 
        return redirect('fpass')

def newpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(mobile=request.session['mobile'])
            if request.POST['npassword'] == request.POST['cnpassword']:
                user.password = request.POST['npassword']
                user.save()
                msg = "Password Updated Successfully!!"
                return render(request, 'login.html', {'msg': msg})
            else:
                msg = "New password & confirm new password do not match!!"
                return render(request, 'newpass.html', {'msg': msg})
        except User.DoesNotExist:
            msg = "User not found!!"
            return render(request, 'newpass.html', {'msg': msg})
        except Exception as e:
            print(e)
            msg = "An error occurred. Please try again."
            return render(request, 'newpass.html', {'msg': msg})
    else:
        return render(request, 'newpass.html')

def profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)
    return render(request, "profile.html", {"user": user})

def book_appointment(request):
    return render(request, 'book_appointment.html')  # or your template name



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # success URL
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# myapp/views.py


def passenger(request):
    return render(request, 'passenger.html')

def passengernew(request):
    return render(request, 'passengernew.html')


def passenger_form(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        passenger = PassengerPass.objects.create(
            route_type=data.get('route_type'),
            first_name=data.get('first_name'),
            email=data.get('email'),
            mobile=data.get('mobile'),
            address=data.get('address'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            from_location=data.get('from_location'),
            to_location=data.get('to_location'),
            distance_km=data.get('distance_km'),
            pass_type=data.get('pass_type'),
            duration_months=data.get('duration_months'),
            from_date=data.get('from_date'),
            to_date=data.get('to_date'),
            amount=data.get('amount'),
            photo=files.get('photo'),
            light_bill=files.get('light_bill'),
            aadhaar=files.get('aadhaar'),
        )

        # use passenger.id instead of unique_id
        return redirect(f'/payment_gateway/?name={passenger.first_name}&amount={passenger.amount}&uid={passenger.id}')
    return render(request, 'passenger.html')


def payment_gateway(request):
    name = request.GET.get('name')
    amount = request.GET.get('amount')
    uid = request.GET.get('uid')  # still passing id
    return render(request, 'payment_gateway.html', {
        'name': name,
        'amount': amount,
        'uid': uid
    })


def payment_success(request):
    uid = request.GET.get('uid')
    return render(request, 'passenger_form.html', {
        'unique_id': uid,
        'show_pdf': True,
    })


def generate_pdf(request, uid):
    passenger = PassengerPass.objects.get(id=uid)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PassengerPass_{passenger.id}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, height - 50, "Passenger Bus Pass Receipt")

    p.setFont("Helvetica", 12)
    y = height - 100

    details = [
        f"Full Name: {passenger.first_name}",
        f"Email: {passenger.email}",
        f"Mobile: {passenger.mobile}",
        f"Address: {passenger.address}",
        f"DOB: {passenger.dob}",
        f"Gender: {passenger.gender}",
        f"Route Type: {passenger.route_type}",
        f"From: {passenger.from_location} To: {passenger.to_location}",
        f"Distance: {passenger.distance_km} KM",
        f"Pass Type: {passenger.pass_type}",
        f"Duration: {passenger.duration_months} Month(s)",
        f"From Date: {passenger.from_date}",
        f"To Date: {passenger.to_date}",
        f"Amount Paid: ₹{passenger.amount}",
    ]

    for line in details:
        p.drawString(50, y, line)
        y -= 20

    # Add photo if available
    if passenger.photo:
        photo_path = os.path.join(settings.MEDIA_ROOT, passenger.photo.name)
        if os.path.exists(photo_path):
            p.drawImage(photo_path, width - 150, height - 300, width=100, height=120)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response




def clgstudentnew(request):  # New or Renewal selection page
    return render(request, 'clgstudentnew.html')



def clgstudentform(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        student = CollegeStudentPass.objects.create(
            route_type = data.get('route_type'),
            ent_number = data.get('ent_number'),
            first_name = data.get('first_name'),
            email = data.get('email'),
            mobile = data.get('mobile'),
            address = data.get('address'),
            dob = data.get('dob'),
            clg_name = data.get('clg_name'),
            clg_address = data.get('clg_address'),
            sem = data.get('sem'),
            gender = data.get('gender'),
            from_location = data.get('from_location'),
            to_location = data.get('to_location'),
            distance_km = data.get('distance_km'),
            pass_type = data.get('pass_type'),
            duration_months = data.get('duration_months'),
            from_date = data.get('from_date'),
            to_date = data.get('to_date'),
            amount = data.get('amount'),
            photo = files.get('photo'),
            light_bill = files.get('light_bill'),
            aadhaar = files.get('aadhaar'),
            provisional = files.get('provisional'),
            fee_receipt = files.get('fee_receipt'),
            payment_mode = data.get('payment_mode'),
        )

        if student.payment_mode == "Online":
            return redirect('clgstudentpayment', id=student.id)
        else:
            return redirect('clgstudentreceipt', id=student.id)

    return render(request, 'clgstudentform.html')




def clgstudentform1(request):  # New or Renewal selection page
    return render(request, 'clgstudentform1.html')

def clgstudentpayment(request, id):
    student = get_object_or_404(CollegeStudentPass, id=id)
    return render(request, 'clgstudentpayment.html', {
        'name': student.first_name,
        'amount': student.amount,
        'uid': student.id,
    })

def clgstudentreceipt(request, id):
    student = get_object_or_404(CollegeStudentPass, id=id)
    return render(request, 'clgstudentreceipt.html', {'student': student})




def student_form_view(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        student = StudentPass.objects.create(
            route_type=data['route_type'],
            roll_number=data['roll_number'],
            first_name=data['first_name'],
            email=data['email'],
            mobile=data['mobile'],
            address=data['address'],
            dob=data['dob'],
            gender=data['gender'],
            school_name=data['school_name'],
            school_address=data['school_address'],
            standard=data['standard'],
            from_location=data['from_location'],
            to_location=data['to_location'],
            distance_km=data['distance_km'],
            pass_type=data['pass_type'],
            duration_months=data['duration_months'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            amount=data['amount'],
            photo=files['photo'],
            light_bill=files['light_bill'],
            aadhaar=files['aadhaar'],
            provisional=files['provisional'],
            payment_mode=data['payment_mode']
        )

        return redirect('student_success', student_id=student.id)
    return render(request, 'studentform.html')


def student_success_view(request, student_id):
    student = StudentPass.objects.get(id=student_id)
    return render(request, 'studentform1.html', {'student': student})



def generate_student_pdf(request, student_id):
    student = StudentPass.objects.get(id=student_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="StudentBusPass_{student.roll_number}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Student Bus Pass Receipt")

    p.setFont("Helvetica", 12)
    y = height - 100
    p.drawString(50, y, f"Name: {student.first_name}")
    p.drawString(50, y - 20, f"Roll No: {student.roll_number}")
    p.drawString(50, y - 40, f"Email: {student.email}")
    p.drawString(50, y - 60, f"Mobile: {student.mobile}")
    p.drawString(50, y - 80, f"From: {student.from_location} To: {student.to_location}")
    p.drawString(50, y - 100, f"Distance: {student.distance_km} km")
    p.drawString(50, y - 120, f"Amount Paid: ₹{student.amount}")
    p.drawString(50, y - 140, f"Pass Type: {student.pass_type}")
    p.drawString(50, y - 160, f"Duration: {student.duration_months} months")
    p.drawString(50, y - 180, f"Payment Mode: {student.payment_mode}")

    # Photo
    if student.photo:
        photo_path = os.path.join(settings.MEDIA_ROOT, student.photo.name)
        if os.path.exists(photo_path):
            p.drawImage(photo_path, width - 150, height - 250, width=80, height=100)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
