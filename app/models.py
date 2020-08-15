from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

#----------------login------------------------------------------------------------

class login_tb(models.Model):
    lid=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    usertype=models.CharField(max_length=30)

class recep(models.Model):
    rlid=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    hos_id=models.IntegerField()
    hos=models.CharField(max_length=30)
    place=models.CharField(max_length=30)


#--------------------ADMIN------------------------------------------------------------

class admin_tb(models.Model):
    lid=models.IntegerField(primary_key=True)
    hos=models.IntegerField()
    pat=models.IntegerField()
    lab=models.IntegerField()
    phar=models.IntegerField()
    out_lab=models.IntegerField()
    out_phar=models.IntegerField()
    out_hosp=models.IntegerField()

class hosp_tb(models.Model):
    lid=models.IntegerField(primary_key=True)
    doc=models.IntegerField()
    pha=models.IntegerField()
    lab=models.IntegerField()

#--------Hospital------------------------------------------------------------

class hosp_regis(models.Model):
    hid=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    cont_name=models.CharField(max_length=10)
    ph_no=models.IntegerField()
    email=models.CharField(max_length=30)
    address=models.TextField(max_length=120)
    website=models.CharField(max_length=30)
class out_hosptital_regis(models.Model):
    hid=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=50)
    cont_name=models.CharField(max_length=30)
    ph_no=models.IntegerField()
    email=models.CharField(max_length=30)
    address=models.TextField(max_length=120)
    website=models.CharField(max_length=20)
    user=models.CharField(max_length=30,default="none")
    passw=models.CharField(max_length=30,default="none")

#--------Doctor------------------------------------------------------------

class doc_regis(models.Model):
    did=models.IntegerField(primary_key=True)
    hid=models.IntegerField()
    lid=models.IntegerField()
    hos=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    gender=models.CharField(max_length=10)
    dob=models.CharField(max_length=10)
    qual=models.CharField(max_length=30)
    special=models.CharField(max_length=10)
    exper=models.IntegerField()
    email=models.CharField(max_length=30)
    phone=models.IntegerField()
    user=models.CharField(max_length=30)
    passw=models.CharField(max_length=30)
    avail=models.CharField(max_length=30)

#--------Patient------------------------------------------------------------

class patient_regis(models.Model):
    pid=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    gender=models.CharField(max_length=10)
    dob=models.DateField(null=True)
    ph_no=models.IntegerField()
    bld=models.CharField(max_length=30,default="B +ve")
    email=models.CharField(max_length=30)
    address=models.TextField(max_length=120)
    user=models.CharField(max_length=30,default="none")
    passw=models.CharField(max_length=30,default="none")
    age=models.IntegerField()
    date=models.DateField()
    pic=models.ImageField('profile picture', upload_to='static/patient/images/', null=True, blank=True)

    
#--------Pharmacy------------------------------------------------------------

class phar_regis(models.Model):
    phid=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    cont_name=models.CharField(max_length=10)
    address=models.TextField(max_length=120)
    ph_no=models.IntegerField()
    email=models.CharField(max_length=30)
class out_phar_regis(models.Model):
    phid=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    cont_name=models.CharField(max_length=10)
    ph_no=models.IntegerField()
    email=models.CharField(max_length=30)
    address=models.TextField(max_length=120)
    user=models.CharField(max_length=30,default="none")
    passw=models.CharField(max_length=30,default="none")
    
#--------Lab------------------------------------------------------------
class lab_regis(models.Model):
    lab_id=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    cont_name=models.CharField(max_length=10)
    address=models.TextField(max_length=120)
    ph_no=models.IntegerField()
    email=models.CharField(max_length=30)
class out_lab_regis(models.Model):
    lab_id=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    cont_name=models.CharField(max_length=10)
    ph_no=models.IntegerField()
    email=models.CharField(max_length=30)
    address=models.TextField(max_length=120)
    user=models.CharField(max_length=30,default="none")
    passw=models.CharField(max_length=30,default="none")

#-----------------------------hospital pharmacy----------------------------------------------

class hos_phar(models.Model):
    phid=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    cont_name=models.CharField(max_length=10)
    ph_no=models.IntegerField()
    address=models.TextField(max_length=120)
    email=models.CharField(max_length=30)
    user=models.CharField(max_length=30,default="none")
    passw=models.CharField(max_length=30,default="none")

#-------------------------------hospital lab-------------------------------------------------

class hos_lab(models.Model):
    lab_id=models.IntegerField(primary_key=True)
    lid=models.IntegerField()
    name=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    cont_name=models.CharField(max_length=10)
    ph_no=models.IntegerField()
    email=models.CharField(max_length=30)
    user=models.CharField(max_length=30,default="none")
    passw=models.CharField(max_length=30,default="none")
#---------------------------Booking-------------------------------------------------------------------------------
class booking_tb(models.Model):
    #pid=lid(inserted)
    bid=models.IntegerField(primary_key=True)
    pid=models.IntegerField()
    did=models.IntegerField()
    location=models.CharField(max_length=50)
    specialization=models.CharField(max_length=30)
    time=models.CharField(max_length=30)
    date=models.DateField()
    hid=models.IntegerField()
    name=models.CharField(max_length=30)
    age=models.IntegerField()
    gender=models.CharField(max_length=30)
    place=models.CharField(max_length=50)
    hosp_name=models.CharField(max_length=50)
    dr_name=models.CharField(max_length=50)
    status=models.CharField(max_length=30)

class lab_tb(models.Model):
    llid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    pid=models.CharField(max_length=30)
    test=models.CharField(max_length=30)
    doc=models.CharField(max_length=30)
    hos=models.CharField(max_length=30)
    date=models.CharField(max_length=30)
    result=models.FileField(null=True,blank=True)
    pat=models.CharField(max_length=30)

class phar_tb(models.Model):
    llid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    pid=models.CharField(max_length=30)
    med=models.CharField(max_length=30)
    disease=models.CharField(max_length=30)
    doc=models.CharField(max_length=30)
    hos=models.CharField(max_length=30)
    date=models.CharField(max_length=30)
    timing=models.CharField(max_length=30)
    days=models.IntegerField()
    pat=models.CharField(max_length=30)

#--------------------------------------medicine stock---------------------------------------------------

class med_stock(models.Model):
    mlid=models.IntegerField(primary_key=True)
    f_date=models.CharField(max_length=30)
    e_date=models.CharField(max_length=30)
    med=models.CharField(max_length=30)
    disease=models.CharField(max_length=30)
    stock=models.IntegerField()
    lid=models.IntegerField()
    ph_no=models.IntegerField()
    address=models.TextField(max_length=120)
    hos=models.CharField(max_length=30)
    place=models.CharField(max_length=30)

    def __str__(self):
        return self.med
    
