import random

from django.db import models
from django.utils import timezone


# Existing models
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    mobile = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=20)



    def __str__(self):
        return self.name





class PassengerPass(models.Model):
    ROUTE_CHOICES = (('Single', 'Single'), ('Multiple', 'Multiple'))
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    PASS_TYPE_CHOICES = (('Local', 'Local'), ('Express', 'Express'))

    route_type = models.CharField(max_length=20, choices=ROUTE_CHOICES)
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    address = models.TextField()
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    distance_km = models.FloatField()
    pass_type = models.CharField(max_length=20, choices=PASS_TYPE_CHOICES)
    duration_months = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='photos/')
    light_bill = models.FileField(upload_to='documents/light_bills/')
    aadhaar = models.FileField(upload_to='documents/aadhaars/')
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.mobile}"


class CollegeStudentPass(models.Model):
    ROUTE_CHOICES = [
        ('Single', 'Single'),
        ('Multiple', 'Multiple'),
    ]

    PASS_TYPE_CHOICES = [
        ('Local', 'Local'),
        ('Express', 'Express'),
    ]

    DURATION_CHOICES = [
        ('1', '1 Month'),
        ('3', '3 Months'),
        ('6', '6 Months'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('Online', 'Online'),
    ]

    route_type = models.CharField(max_length=20, choices=ROUTE_CHOICES)
    ent_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    address = models.TextField()
    dob = models.DateField()
    clg_name = models.CharField(max_length=255)
    clg_address = models.TextField()
    sem = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    distance_km = models.FloatField()
    pass_type = models.CharField(max_length=20, choices=PASS_TYPE_CHOICES)
    duration_months = models.CharField(max_length=2, choices=DURATION_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    photo = models.ImageField(upload_to='uploads/photos/')
    light_bill = models.FileField(upload_to='uploads/light_bills/')
    aadhaar = models.FileField(upload_to='uploads/aadhaar/')
    provisional = models.FileField(upload_to='uploads/provisional/')
    fee_receipt = models.FileField(upload_to='uploads/fee_receipts/')
    
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ent_number} - {self.first_name}"


class StudentPass(models.Model):
    route_type = models.CharField(max_length=20)
    roll_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    address = models.TextField()
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    school_name = models.CharField(max_length=200)
    school_address = models.TextField()
    standard = models.CharField(max_length=10)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    pass_type = models.CharField(max_length=20)
    duration_months = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='student_photos/')
    light_bill = models.FileField(upload_to='light_bills/')
    aadhaar = models.FileField(upload_to='aadhaar_docs/')
    provisional = models.FileField(upload_to='provisional_docs/')
    payment_mode = models.CharField(max_length=20)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roll_number} - {self.first_name}"


class Appointment(models.Model):
    CATEGORY_CHOICES = [
        ("Color", "Color"),
        ("Color and Haircut", "Color and Haircut"),
        ("Hair Treatments", "Hair Treatments"),
        ("Haircuts", "Haircuts"),
        ("Nail Treatments", "Nail Treatments"),
        ("Facials", "Facials"),
        ("Waxing", "Waxing"),
        ("All Treatments", "All Treatments"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.BigIntegerField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    appointment_time = models.TimeField()
    appointment_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.category} on {self.appointment_date} at {self.appointment_time}"
    











 