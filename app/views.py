from django.shortcuts import render
from app.models import *
from django.db.models import Avg, Max, Min, Sum, Count
import json
from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core import serializers
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
import random
import smtplib
import os
import numpy as np

# Read QR Code
from pyzbar.pyzbar import decode
from PIL import Image
import pyqrcode
import cv2

# Create your views here.
def home(request):
    return render(request,"index.html",{})
def index(request):
    return render(request,"index.html",{})
def hos_list(request):
    return render(request,"hospital/list.html",{})
def register(request):
    return render(request,"reg.html",{})
def out(request):
    print ("logout_fn")
    if request.session.has_key('uid'):
        user=login_tb.objects.filter(lid=request.session['uid'])
        for i in user:
            typ=i.usertype
        print ("session=: deleting ",request.session['uid'])
        if request.session.has_key('uid') and typ=="doctor":
            data=doc_regis.objects.get(lid=request.session['uid'])
            data.avail="Not Available"
            data.save()
        del request.session['uid']
        print ("session deleted")
        return render(request,"index.html",{})
def login(request):
    return render(request,"log.html",{})
def hosp(request):
    return render(request,"hos.html",{})
def lab(request):
    return render(request,"lab.html",{})
def phar(request):
    return render(request,"phar.html",{})
def forget_pass(request):
    return render(request,"forgotpassword.html",{})
def stk_med(request):
    return render(request,"med_check.html",{})
def appoit(request):
    return render(request,"hospital/add_rec.html",{})

#-----------------------out_pharm reg-------------------------------------------------------------

def phar_reg(request):
    print ("in phar_reg")
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("loc")
        c=request.POST.get("cname")
        d=request.POST.get("phone")
        e=request.POST.get("email")
        h=request.POST.get("web")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        h=request.POST.get("out")
        r=request.POST.get("add")
        print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g,r)
        amt=login_tb.objects.filter(username=f)
        am=out_phar_regis.objects.filter(user=f)
        print("amt",amt.count(),"am",am.count())
        if(amt.count()==0):
            if(am.count()>=1):
                return HttpResponse("<script>alert('Username already exist. choose another');window.location.href='/phar/';</script>")
        else:
            return HttpResponse("<script>alert('Username already used. choose another');window.location.href='/phar/';</script>")
        ar=phar_regis.objects.filter(name=a,place=b)
        aa=out_phar_regis.objects.filter(name=a,place=b)
        if(ar.count()>=1 or aa.count()>=1):
            return HttpResponse("<script>alert('pharmacy account already exist. please login with username and password');window.location.href='/login/';</script>")  
        obj=phar_regis.objects.filter(name=a,place=b,email=e)
        print("out hos",obj.count())
        if(obj.count()==0):
            obj=out_phar_regis(name=a,place=b,lid=0,cont_name=c,ph_no=d,email=e,user=f,passw=g,address=r)
            obj.save()
            print("out lab is stored")
            if str(h)=="out":
                email = EmailMessage('Verification needed','Hi'+' '+str(c)+','+'\n'+'mail the documents'+'\n'+'1. Pharmacy certificates'+'\n'+'2. owner name and address'+'\n'+'3. Pharmacy address', to=[e])
                email.send()
                return HttpResponse("<script>alert('successfully Registered. email the concerned document and wait for admin approval');window.location.href='/index/';</script>")
        else:
            return HttpResponse("<script>alert('Already Registered. Pls login with username and password');window.location.href='/login/';</script>")

def app_pha(request):
    print ("admin_pha_vw")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        pha=out_phar_regis.objects.all()
        print (request.session['uid'])
        return render(request,"admin/out_pha_admin_view.html",{"pha":pha})
    return HttpResponse("<script>alert('Please Login as admin');window.location.href='/login/';</script>")

def aprove_pha(request):
    print("aprove")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        if request.method=="POST":
            a=request.POST.get("phaname")
            b=request.POST.get("loc")
            c=request.POST.get("cont_name")
            d=request.POST.get("cont_no")
            e=request.POST.get("email")
            f=request.POST.get("uname")
            g=request.POST.get("pass")
            h=request.POST.get("out")
            print(h)
            print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g)
            obj=login_tb(
                username=f,password=g,usertype="out_pharmacy"
                )
            obj.save()
            cnt=login_tb.objects.filter(username=f,password=g)
            print ("phar cnt ",cnt.count())
            if cnt.count()==1:
                user=login_tb.objects.get(username=f,password=g)
                l_id=user.lid
                print ("l_id===================",l_id)
                obj=phar_regis(
                    lid=l_id,name=a,place=b,cont_name=c,ph_no=d,email=e
                    )
                obj.save()
                tt=out_phar_regis.objects.get(lid=0)
                ar=phar_regis.objects.get(lid=l_id)
                print(tt,ar)
                ar.address=tt.address
                ar.save()
                ob=out_phar_regis.objects.filter(name=a,place=b,email=e)
                ob.delete()
                print ("registered")
                if str(h)=="out":
                    email = EmailMessage('Status of Registration','Hi'+' '+str(c)+','+'\n'+'\n'+'Your pharmacy account has been activated. Please login to continue'+'\n'+'user name is:'+' '+str(f)+'\n'+'password is:'+' '+str(g), to=[e])
                    email.send()
                return  HttpResponse("<script>alert('Registration Successful');window.location.href='/main/';</script>")
            else:
                 return HttpResponse("<script>alert('User already exist, please register with another username');window.location.href='/index/';</script>")
    return HttpResponse("<script>alert('Please Login');window.location.href='/login/';</script>")

def aa_o_pha_hm(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="out_pharmacy":
        data=phar_regis.objects.get(lid=c)
        print(request.session['uid'])
        return render(request,"pharmacy/out/out_phar_hmlog.html",{"user":data})
    else:
        return HttpResponse("<script>alert('Please login using lab username and password');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login using lab username and password');window.location.href='/login/';</script>")

def kout_presc_pha(request):
    c=request.session['uid']
    global pat
    print("checkqr")
    val="9"
    s=request.FILES["files"]
    if s:
        fs=  FileSystemStorage("app\\static\\res")
        try:
            os.remove("app\\static\\res\\out.png")
        except:
            pass
        fs.save("out.png",s)
        try:
            img = cv2.imread('app\\static\\res\\out.png')
            d = decode(img)
            val=d[0].data.decode('ascii')
           
        except Exception as e:
            print("cannot read",e)
    print("Value: ",val)
    pat=int(val)
    user=phar_regis.objects.get(lid=c)
    obb=patient_regis.objects.filter(lid=int(val))
    if(obb.count()==0):
        return HttpResponse("<script>alert('No Data Available. check crct qr');window.location.href='/aa_o_pha_hm/';</script>")
    else:
        ob=patient_regis.objects.get(lid=int(val))
    from datetime import date
    today = date.today()
    ob.date=today
    dates=ob.dob
    ag = int(today.year) - int(dates.year)
    ob.age=ag
    name=user.name
    pre=phar_tb.objects.all().filter(pid=int(val),name="Not visited").order_by('-date')
    return render(request,"pharmacy/out/out_qrcode_after.html",{"data":ob,"user":user,"name":name,"phar":pre})

def mout_pstatus(request):
    c=request.session['uid']
    user=phar_regis.objects.get(lid=c)
    a=request.POST.get("date")
    b=request.POST.get("hos")
    z=request.POST.get("pharm")
    d=request.POST.get("pt")
    e=request.POST.get("doc")
    mm=request.POST.get("med")
    time=request.POST.get("t")
    day=request.POST.get("d")
    f=request.POST.get("llid")
    sums=0
    for i in range (0,5,2):
        sums=sums+int(time[i])
    print(sums)
    s=sums*int(day)
    print(s)
    da=med_stock.objects.filter(med=mm)
    if (da.count()==0):
        return HttpResponse("<script>alert('Medicine not Added');window.location.href='/aa_o_pha_hm/';</script>")
    if (da.count()==1):
        st=med_stock.objects.get(med=mm,hos=z)
        aa=st.stock
        new=int(aa)-int(s)
        st.stock=new
        st.save()
        obj=phar_tb.objects.get(pid=d,doc=e,date=a,hos=b,llid=f)
        obj.name=user.name
        obj.save()
    #return render(request,"pharmacy/phar_hmlog.html",{"user":user})
        return HttpResponse("<script>alert('Prescription Successfully Provided');window.location.href='/aa_o_pha_hm/';</script>")

def vv_med_add(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="out_pharmacy":
        user=phar_regis.objects.get(lid=c)
        return render(request,"pharmacy/out/add_med.html",{"user":user})

def yy_stock(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="out_pharmacy":
        a=request.POST.get("f_date")
        b=request.POST.get("e_date")
        m=request.POST.get("med")
        h=request.POST.get("dis")
        d=request.POST.get("stock")
        ob=phar_regis.objects.get(lid=c)
        e=ob.name
        f=ob.place
        ss=ob.ph_no
        g=ob.lid
        obj=med_stock(f_date=a,e_date=b,med=m,disease=h,lid=g,stock=d,hos=e,place=f,ph_no=ss)
        obj.save()
        obb=med_stock.objects.get(f_date=a,e_date=b,med=m,disease=h,lid=g,stock=d,hos=e,place=f)
        obb.address=ob.address
        obb.save()
        return HttpResponse("<script>alert('Stock Successfully updated');window.location.href='/aa_o_pha_hm/';</script>")

def ee_vw(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="out_pharmacy":
        user=phar_regis.objects.get(lid=c)
        data=med_stock.objects.filter(hos=user.name,place=user.place).order_by('med')
        return render(request,"pharmacy/out/view_medicine.html",{"user":user,"data":data})



#-----------------------out_hosp reg--------------------------------------------------------------------------------------------

def hosp_reg(request):
    print ("in hos_reg")
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("loc")
        c=request.POST.get("cname")
        d=request.POST.get("phone")
        e=request.POST.get("email")
        h=request.POST.get("web")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        r=request.POST.get("out")
        p=request.POST.get("add")
        print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g,h)
        amt=login_tb.objects.filter(username=f)
        am=out_hosptital_regis.objects.filter(user=f)
        print("amt",amt.count(),"am",am.count())
        if(amt.count()==0):
            if(am.count()>=1):
                return HttpResponse("<script>alert('Username already exist. choose another');window.location.href='/hosp/';</script>")
        else:
            return HttpResponse("<script>alert('Username already used. choose another');window.location.href='/hosp/';</script>")
        ar=hosp_regis.objects.filter(name=a,place=b)
        aa=out_hosptital_regis.objects.filter(name=a,place=b)
        if(ar.count()>=1 or aa.count()>=1):
            return HttpResponse("<script>alert('Hospital account already exist. please login with username and password');window.location.href='/login/';</script>")
        obj=hosp_regis.objects.filter(name=a,place=b,email=e)
        print("out hos",obj.count())
        if(obj.count()==0):
            obj=out_hosptital_regis(name=a,place=b,lid=0,cont_name=c,ph_no=d,email=e,website=h,user=f,passw=g,address=p)
            obj.save()
            print("out hosp is stored")
            if str(r)=="out":
                email = EmailMessage('Verification needed','Hi'+' '+str(c)+','+'\n'+'mail the documents' +'\n'+ '1. Hospital certificates'+ '\n'+'2. owner name and address' +'\n'+'3. Hospital address', to=[e])
                email.send()
                return HttpResponse("<script>alert('successfully Registered. mail the concern documents and wait for admin approval');window.location.href='/index/';</script>")
        else:
            return HttpResponse("<script>alert('Already Registered. Pls login with username and password');window.location.href='/login/';</script>")

def app_hos(request):
    print ("admin_hospital_vw")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        hosp=out_hosptital_regis.objects.all()
        print (request.session['uid'])
        return render(request,"admin/out_hos_admin_view.html",{"hospital":hosp})
    return HttpResponse("<script>alert('Please Login as admin');window.location.href='/login/';</script>")


def aprove_hos(request):
    print("aprove")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        if request.method=="POST":
            a=request.POST.get("hosname")
            b=request.POST.get("loc")
            c=request.POST.get("cont_name")
            d=request.POST.get("cont_no")
            e=request.POST.get("email")
            f=request.POST.get("uname")
            g=request.POST.get("pass")
            h=request.POST.get("out")
            i=request.POST.get("web")
            print(h)
            print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g)
            obj=login_tb(
                username=f,password=g,usertype="hospital"
                )
            obj.save()
            cnt=login_tb.objects.filter(username=f,password=g)
            if cnt.count()==1:
                user=login_tb.objects.get(username=f,password=g)
                l_id=user.lid
                print ("l_id===================",l_id)
                obj=hosp_regis(
                    lid=l_id,name=a,place=b,cont_name=c,ph_no=d,email=e,website=str(i)
                    )
                obj.save()
                q=0
                r=0
                x=0
                obb=hosp_tb(lid=l_id,doc=q,lab=r,pha=x)
                obb.save()
                tt=out_hosptital_regis.objects.get(lid=0,name=a)
                am=hosp_regis.objects.get(lid=l_id)
                print(tt,am)
                am.address=tt.address
                am.save()
                ob=out_hosptital_regis.objects.filter(name=a,place=b,email=e)
                ob.delete()
                if str(h)=="out":
                    email = EmailMessage('Status of Registration','Hi'+' '+str(c)+','+'\n'+'\n'+'Your Hospital account has been activated. Please login to continue'+'\n'+'user name is:' + str(f) +'\n'+'password is:' +str(g), to=[e])
                    email.send()
                    print ("registered")
                    return  HttpResponse("<script>alert('Registration Successful');window.location.href='/main/';</script>")
            else:
                 return HttpResponse("<script>alert('User already exist, please register with another username');window.location.href='/index/';</script>")
    return HttpResponse("<script>alert('Please Login as admin');window.location.href='/login/';</script>")



#-----------------------out_lab reg----------------------------------------------------------------------------------

def lab_reg(request):
    print ("in out_lab_reg")
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("loc")
        c=request.POST.get("cname")
        d=request.POST.get("phone")
        e=request.POST.get("email")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        h=request.POST.get("out")
        r=request.POST.get("add")
        print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g)
        amt=login_tb.objects.filter(username=f)
        am=out_lab_regis.objects.filter(user=f)
        print("amt",amt.count(),"am",am.count())
        if(amt.count()==0):
            if(am.count()>=1):
                return HttpResponse("<script>alert('Username already exist. choose another');window.location.href='/lab/';</script>")
        else:
            return HttpResponse("<script>alert('Username already used. choose another');window.location.href='/lab/';</script>")
        ar=lab_regis.objects.filter(name=a,place=b)
        aa=out_lab_regis.objects.filter(name=a,place=b)
        if(ar.count()>=1 or aa.count()>=1):
            return HttpResponse("<script>alert('laboratory account already exist. please login with username and password');window.location.href='/login/';</script>")
        obj=lab_regis.objects.filter(name=a,place=b,email=e)
        print("out hos",obj.count())
        if(obj.count()==0):
            obj=out_lab_regis(name=a,place=b,lid=0,cont_name=c,ph_no=d,email=e,user=f,passw=g,address=r)
            obj.save()
            print("out lab is stored")
            if(str(h)=="out"):
                email = EmailMessage('Verification needed','Hi'+' '+str(c)+','+'\n'+'mail the documents' +'\n'+ '1. Laboratory certificates'+ '\n'+'2. owner name and address' +'\n'+'3. Laboratory address', to=[e])
                email.send()
                return HttpResponse("<script>alert('successfully Registered. email the concerned document and wait for admin approval');window.location.href='/index/';</script>")
        else:
            return HttpResponse("<script>alert('Already Registered. Pls login with username and password');window.location.href='/login/';</script>")

def app_lab(request):
    print ("admin_lab_vw")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        lab=out_lab_regis.objects.all()
        print (request.session['uid'])
        return render(request,"admin/out_lab_admin_view.html",{"lab":lab})
    return HttpResponse("<script>alert('Please Login as admin');window.location.href='/login/';</script>")

def aprove_lab(request):
    print("aprove")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        if request.method=="POST":
            a=request.POST.get("labname")
            b=request.POST.get("loc")
            c=request.POST.get("cont_name")
            d=request.POST.get("cont_no")
            e=request.POST.get("email")
            f=request.POST.get("uname")
            g=request.POST.get("pass")
            h=request.POST.get("out")
            print(h)
            print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g)
            obj=login_tb(
                username=f,password=g,usertype="out_laboratory"
                )
            obj.save()
            cnt=login_tb.objects.filter(username=f,password=g)
            print ("phar cnt ",cnt.count())
            if cnt.count()==1:
                user=login_tb.objects.get(username=f,password=g)
                l_id=user.lid
                print ("l_id===================",l_id)
                obj=lab_regis(
                    lid=l_id,name=a,place=b,cont_name=c,ph_no=d,email=e
                    )
                obj.save()
                tt=out_lab_regis.objects.get(lid=0)
                ar=lab_regis.objects.get(lid=l_id)
                print(tt,ar)
                ar.address=tt.address
                ar.save()
                ob=out_lab_regis.objects.filter(name=a,place=b,email=e)
                ob.delete()
                if str(h)=="out":
                    email = EmailMessage('Status of Registration','Hi'+' '+str(c)+','+'\n'+'\n'+'Your Laboratory account has been activated. Please login to continue'+'\n'+'user name is:'+' '+str(f)+'\n'+'password is:'+' '+str(g), to=[e])
                    email.send()
                print ("registered")
                return  HttpResponse("<script>alert('Registration Successful');window.location.href='/main/';</script>")
            else:
                 return HttpResponse("<script>alert('User already exist, please register with another username');window.location.href='/index/';</script>")
    return HttpResponse("<script>alert('Please Login as admin');window.location.href='/login/';</script>")

def o_labo_hm(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="out_laboratory":
        data=lab_regis.objects.get(lid=c)
        print(request.session['uid'])
        return render(request,"lab/out/out_lab_hmlog.html",{"user":data})
    else:
        return HttpResponse("<script>alert('Please login using lab username and password');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login using lab username and password');window.location.href='/login/';</script>")

def ot_tst_lab(request):
    c=request.session['uid']
    global pat
    print("checkqr")
    val="9"
    s=request.FILES["files"]
    if s:
        fs=  FileSystemStorage("app\\static\\res")
        try:
            os.remove("app\\static\\res\\out.png")
        except:
            pass
        fs.save("out.png",s)
        try:
            img = cv2.imread('app\\static\\res\\out.png')
            d = decode(img)
            val=d[0].data.decode('ascii')
           
        except Exception as e:
            print("cannot read",e)
    print("Value: ",val)
    pat=int(val)
    user=lab_regis.objects.get(lid=c)
    obb=patient_regis.objects.filter(lid=int(val))
    if(obb.count()==0):
        return HttpResponse("<script>alert('No Data Available. check crct qr');window.location.href='/doct_hm/';</script>")
    else:
        ob=patient_regis.objects.get(lid=int(val))
    from datetime import date
    today = date.today()
    ob.date=today
    dates=ob.dob
    ag = int(today.year) - int(dates.year)
    ob.age=ag
    ob.save()
    lab=lab_tb.objects.all().filter(pid=int(val),name="Not visited").order_by('-date')
    return render(request,"lab/out/out_qrcode_after_lab.html",{"data":ob,"user":user,"lab":lab})

def aout_info(request):
    a=request.POST.get("date")
    b=request.POST.get("test")
    d=request.POST.get("pt")
    e=request.POST.get("doc")
    f=request.POST.get("llid")
    g=request.POST.get("hos")
    print(a,b,d,e,f,g)
    obj=lab_tb.objects.get(pid=d,doc=e,date=a,hos=g,test=b,llid=f)
    return render(request,"lab/out/upload.html",{"data":obj})

def bout_file_lab(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        print(c)
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="out_laboratory":
        a=request.POST.get("pid")
        b=request.POST.get("pat")
        f=request.POST.get("test")
        d=request.POST.get("hos")
        user=lab_regis.objects.get(lid=c)
        if request.method=='POST':
            upload_file=request.FILES['document']
            fs=FileSystemStorage()
            obj=lab_tb.objects.get(pid=a,pat=b,name="Not visited",hos=d,test=f)
            obj.result=upload_file
            obj.name=user.name
            obj.save()
            return HttpResponse("<script>alert('Result uploaded successfully');window.location.href='/o_labo_hm/';</script>")



#--------------------patient registration------------------------------------------------------------
        
def patient_reg(request):
    print ("in patient_reg")
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("loc")
        c=request.POST.get("gender")
        d=request.POST.get("phone")
        e=request.POST.get("email")
        h=request.POST.get("bld")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        r=request.POST.get("date")
        m=request.POST.get("add")
        print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g,h)
        amt=login_tb.objects.filter(username=f)
        print("amt",amt.count())
        aa=patient_regis.objects.filter(email=e)
        if(aa.count()>=1):
            return HttpResponse("<script>alert('email already Exist .Choose another email');window.location.href='/register/';</script>")
        if(amt.count()==0):
            obj=login_tb(username=f,password=g,usertype="patient")
            obj.save()
        else:
            return HttpResponse("<script>alert('Username already Exist .Choose another username');window.location.href='/register/';</script>")
##        cv2.imshow('generated_png',img)
##        cv2.waitKey(0)
        cnt=login_tb.objects.filter(username=f,password=g)
        print ("phar cnt ",cnt.count())
        if cnt.count()==1:  
            user=login_tb.objects.get(username=f,password=g)
            l_id=user.lid
            print ("l_id===================",l_id)
            msg=str(l_id)
            otptstr= ""
            for i in msg:
                num = ord(i)
                if (num >=0) :
                    if (num <= 127):
                        otptstr= otptstr + i
            msg=otptstr
            print("The Required output is:",msg)
            print(len(msg))
            qr = pyqrcode.create(msg)
            qr.png('app/qrcode/'+f+'.png', scale=8)
            img = cv2.imread('app/qrcode/'+f+'.png', 0)
            img=cv2.resize(img, (150, 150)) 
            cv2.imwrite('app/qrcode/'+f+'.png', img)
            from datetime import date
            today = date.today()
            obj=patient_regis(
                lid=l_id,name=a,place=b,gender=c,ph_no=d,email=e,bld=str(h),user=f,passw=g,dob=r,address=m,age=0,date=today
                )
            obj.save()
            print ("registered")
            return HttpResponse("<script>alert('Registration Successfull');window.location.href='/index/';</script>")
        else:
            return HttpResponse("<script>alert('User already exist, please register with another username');window.location.href='/index/';</script>")

#------------------------------------login check-------------------------------------------------------------------------------------------------------
        
def login_ck(request):
    print("login check")
    count=0
    if request.method=="POST":
        a=request.POST.get("uname")
        b=request.POST.get("pass")
        print ("un",a,"ps",b)
        user=login_tb.objects.filter(username=a,password=b)
        print (user)
        count=user.count()
#count is counting the number of users in same usrname and password. atleast one is there. if 0 then invalid username and password
        if count==0:
            print ("Invalid User")
            return HttpResponse("<script>alert('Invalid User: enter correct username and password');window.location.href='/login/';</script>")
##            return render(request,"index.html",{"msg":"Invalid User"})
        else:
            for i in user:
                typ=i.usertype
                llid=i.lid
            print ("type",typ,"username",a,"paswd",b,"usercount",count,"userid",llid)
            if count==0 or count>1:
                return HttpResponse("<script>alert('Sorry Database Error');window.location.href='/index/';</script>")
##                return render(request,"index.html",{"msg":"Invalid Userdata"})
            if count==1 and typ=="patient":
                print ("patient page")
                user_dt=patient_regis.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print ("session=: created ",request.session['uid'])
                user_dtt=login_tb.objects.get(lid=request.session['uid'])
                if request.session.has_key('uid'):
                    user=patient_regis.objects.get(user=a,passw=b)
                    print(request.session['uid'])
                    return render(request,"patient/patient_hm.html",{"user":user})
            if count==1 and typ=="admin":
                print ("admin page")
                user_dt=login_tb.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print ("session=: created ",request.session['uid'])
                if request.session.has_key('uid'):
                    data=admin_tb.objects.get(lid=1)
                    print (request.session['uid'])
                    return render(request,"admin/admin_hm.html",{"data":data})
            if count==1 and typ=="hospital":
                print("hospital page")
                user_dt=login_tb.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print("session:= created ", request.session['uid'])
                if request.session.has_key('uid'):
                    data=hosp_regis.objects.get(lid=llid)
                    dat=hosp_tb.objects.get(lid=llid)
                    print(request.session['uid'])
                    return render(request,"hospital/hospital_hm.html",{"data":data,"dat":dat})
            if count==1 and typ=="doctor":
                print("Doctor page")
                user_dt=login_tb.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print("session:= created ", request.session['uid'])
                if request.session.has_key('uid'):
                    data=doc_regis.objects.get(lid=llid)
                    data.avail="Available"
                    data.save()
                    print(request.session['uid'])
                    return render(request,"doctor/dr_homelog.html",{"user":data})
            if count==1 and typ=="laboratory":
                print("lab page")
                user_dt=login_tb.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print("session:= created ", request.session['uid'])
                if request.session.has_key('uid'):
                    data=hos_lab.objects.get(lid=llid)
                    print(request.session['uid'])
                    return render(request,"lab/lab_hmlog.html",{"user":data})
            if count==1 and typ=="out_laboratory":
                print("lab page")
                user_dt=login_tb.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print("session:= created ", request.session['uid'])
                if request.session.has_key('uid'):
                    data=lab_regis.objects.get(lid=llid)
                    print(request.session['uid'])
                    return render(request,"lab/out/out_lab_hmlog.html",{"user":data})
            if count==1 and typ=="pharmacy":
                print("pha page")
                user_dt=login_tb.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print("session:= created ", request.session['uid'])
                if request.session.has_key('uid'):
                    data=hos_phar.objects.get(lid=llid)
                    print(request.session['uid'])
                    return render(request,"pharmacy/phar_hmlog.html",{"user":data})
            if count==1 and typ=="out_pharmacy":
                print("phar page")
                user_dt=login_tb.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print("session:= created ", request.session['uid'])
                if request.session.has_key('uid'):
                    data=phar_regis.objects.get(lid=llid)
                    print(request.session['uid'])
                    return render(request,"pharmacy/out/out_phar_hmlog.html",{"user":data})
            if count==1 and typ=="recept":
                user_dt=login_tb.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print("session:= created ", request.session['uid'])
                if request.session.has_key('uid'):
                    print(request.session['uid'])
                    return render(request,"hospital/booking.html",{})
def reset(request):
    a=request.POST.get("uname")
    b=request.POST.get("email")
    obj=login_tb.objects.filter(username=a)
    if(obj.count()==0):
        return HttpResponse("<script>alert('No account found in that username');window.location.href='/forget_pass/';</script>")
    aa=login_tb.objects.get(username=a)
    if(obj.count()==1):
        c=aa.username
        d=aa.password
        ob=patient_regis.objects.filter(email=b)
        if (ob.count()==1):
            email = EmailMessage('Password for your account','you account username and password are'+'\n'+'username :-'+' '+str(c)+'\n'+'Your account password is :-'+' '+str(d), to=[str(b)])
            email.send()
            return HttpResponse("<script>alert('Your password will be sent to your provided email id');window.location.href='/login/';</script>")
        return HttpResponse("<script>alert('Your entered email is not registered email. please use registered email');window.location.href='/forget_pass/';</script>")
            

#------------ADMIN---------------------------------------------------------

def main(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        data=admin_tb.objects.get(lid=1)
        print (request.session['uid'])
        return render(request,"admin/admin_hm.html",{"data":data})
    else:
        return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
def admin_hos(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        return render(request,"admin/add_hosp.html",{})
    else:
        return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
def admin_lab(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        return render(request,"admin/add_lab.html",{})
    else:
        return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
def admin_pha(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        return render(request,"admin/add_phar.html",{})
    else:
        return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
def adm_hosp(request):
    print ("in admin hospital reg ----> adm_hosp")
    if request.method=="POST":
        a=request.POST.get("hosname")
        b=request.POST.get("loc")
        c=request.POST.get("coname")
        d=request.POST.get("phone")
        e=request.POST.get("email")
        h=request.POST.get("web")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        m=request.POST.get("add")
        print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g,h)
        amt=login_tb.objects.filter(username=f)
        print("amt",amt.count())
        if(amt.count()==0):
            obj=login_tb(username=f,password=g,usertype="hospital")
            obj.save()
        else:
            return HttpResponse("<script>alert('Username alraedy exist. Choose another');window.location.href='/admin_hos/';</script>")
        cnt=login_tb.objects.filter(username=f,password=g)
        print ("phar cnt ",cnt.count())
        if cnt.count()==1:
            user=login_tb.objects.get(username=f,password=g)
            l_id=user.lid
            obj=hosp_regis(
                lid=l_id,name=a,place=b,cont_name=c,ph_no=d,email=e,website=str(h),address=m
                )
            obj.save()
            q=0
            r=0
            x=0
            ob=hosp_tb(lid=l_id,doc=q,lab=r,pha=x)
            ob.save()
            print("registered")
            email = EmailMessage('Hospital Account activated','Hi'+' '+str(c)+','+'\n'+'\n'+'Your Hospital account is created'+'\n'+'USERNAME :'+str(f)+'\n'+'PASSWORD :'+str(g), to=[e])
            email.send()
            return HttpResponse("<script>alert('Hospital successfully added');window.location.href='/admin_hos/';</script>")
    return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
def adm_phar(request):
    print ("in admin pharmacy reg ----> adm_phar")
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("loc")
        c=request.POST.get("coname")
        d=request.POST.get("phone")
        e=request.POST.get("email")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        m=request.POST.get("add")
        print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g)
        amt=login_tb.objects.filter(username=f)
        print("amt",amt.count())
        if(amt.count()==0):
            obj=login_tb(username=f,password=g,usertype="out_pharmacy")
            obj.save()
        else:
            return HttpResponse("<script>alert('Username alraedy exist. Choose another');window.location.href='/admin_pha/';</script>")
        cnt=login_tb.objects.filter(username=f,password=g)
        print ("phar cnt ",cnt.count())
        if cnt.count()==1:
            user=login_tb.objects.get(username=f,password=g)
            l_id=user.lid
            obj=phar_regis(
                lid=l_id,name=a,place=b,cont_name=c,ph_no=d,email=e,address=m
                )
            obj.save()
            email = EmailMessage('Pharmacy Account activated','Hi'+' '+str(c)+','+'\n'+'\n'+'Your Pharmacy account is created'+'\n'+'USERNAME :'+str(f)+'\n'+'PASSWORD :'+str(g), to=[e])
            email.send()
            print("registered")
            return HttpResponse("<script>alert('Pharmacy successfully added');window.location.href='/admin_pha/';</script>")
    return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")
def adm_lab(request):
    print ("in admin lab reg ----> adm_lab")
    if request.method=="POST":
        a=request.POST.get("lab")
        b=request.POST.get("loc")
        c=request.POST.get("coname")
        d=request.POST.get("phone")
        e=request.POST.get("email")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        m=request.POST.get("add")
        print ("a,b,c,d,e,f,g",a,b,c,d,e,f,g)
        amt=login_tb.objects.filter(username=f)
        print("amt",amt.count())
        if(amt.count()==0):
            obj=login_tb(username=f,password=g,usertype="out_laboratory")
            obj.save()
        else:
            return HttpResponse("<script>alert('username alraedy exist. Choose another');window.location.href='/admin_lab/';</script>")
        cnt=login_tb.objects.filter(username=f,password=g)
        print ("phar cnt ",cnt.count())
        if cnt.count()==1:
            user=login_tb.objects.get(username=f,password=g)
            l_id=user.lid
            obj=lab_regis(
                lid=l_id,name=a,place=b,cont_name=c,ph_no=d,email=e,address=m
                )
            obj.save()
            email = EmailMessage('Laboratory Account activated','Hi'+' '+str(c)+','+'\n'+'\n'+'Your Labouratory account is created'+'\n'+'USERNAME :'+str(f)+'\n'+'PASSWORD :'+str(g), to=[e])
            email.send()
            print("registered")
            return HttpResponse("<script>alert('lab successfully added');window.location.href='/admin_lab/';</script>")
    return HttpResponse("<script>alert('Please login using admin username and password');window.location.href='/login/';</script>")

def ad_hosp_vw(request):
    print ("admin_hospital_view")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        hosp=hosp_regis.objects.all()
        print (request.session['uid'])
        return render(request,"admin/admin_hos_view.html",{"hospital":hosp})
    return HttpResponse("<script>alert('Please Login');window.location.href='/index/';</script>")
def ad_lab_vw(request):
    print ("admin_lab_view")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        lab=lab_regis.objects.all()
        print (request.session['uid'])
        return render(request,"admin/admin_lab_view.html",{"lab":lab})
    return HttpResponse("<script>alert('Please Login');window.location.href='/index/';</script>")
def ad_pha_vw(request):
    print ("admin_phar_view")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        pha=phar_regis.objects.all()
        print (request.session['uid'])
        return render(request,"admin/admin_pha_view.html",{"pha":pha})
    return HttpResponse("<script>alert('Please Login');window.location.href='/index/';</script>")
def ad_pat_vw(request):
    print ("admin_phar_view")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="admin":
        pat=patient_regis.objects.all()
        print (request.session['uid'])
        return render(request,"admin/admin_pat_view.html",{"pat":pat})
    return HttpResponse("<script>alert('Please Login');window.location.href='/index/';</script>")
def h_ad_delete(request):
    print("admin hospital delete")
    a=request.POST.get("name")
    b=request.POST.get("loc")
    c=request.POST.get("out")
    e=request.POST.get("email")
    d=request.POST.get("id")
    if(c=="out"):
        email = EmailMessage('Status of Account', 'Your account has been .Terminated. Please contact concern department', to=[e])
        email.send()
    ob=hosp_regis.objects.filter(name=a,place=b,email=e)
    ob.delete()
    obj=login_tb.objects.filter(lid=d)
    obj.delete()
    return HttpResponse("<script>alert('Hospital Successfully Deleted');window.location.href='/main/';</script>")
def l_ad_delete(request):
    print("admin lab delete")
    a=request.POST.get("name")
    b=request.POST.get("loc")
    c=request.POST.get("out")
    e=request.POST.get("email")
    d=request.POST.get("id")
    if(c=="out"):
        email = EmailMessage('Status of Account', 'Your account has been Terminated. Please contact concern department', to=[e])
        email.send()
    ob=lab_regis.objects.filter(name=a,place=b,email=e)
    ob.delete()
    obj=login_tb.objects.filter(lid=d)
    obj.delete()
    return HttpResponse("<script>alert('Laboratory Successfully Deleted');window.location.href='/main/';</script>")
def p_ad_delete(request):
    print("admin phar delete")
    a=request.POST.get("name")
    b=request.POST.get("loc")
    c=request.POST.get("out")
    e=request.POST.get("email")
    d=request.POST.get("id")
    if(c=="out"):
        email = EmailMessage('Status of Account', 'Your account has been Terminated. Please contact concern department', to=[e])
        email.send()
    ob=phar_regis.objects.filter(name=a,place=b,email=e)
    ob.delete()
    obj=login_tb.objects.filter(lid=d)
    obj.delete()
    return HttpResponse("<script>alert('Pharmacy Successfully Deleted');window.location.href='/main/';</script>")
def refresh(request):
    print("refresh")
    aa=hosp_regis.objects.all()
    ab=patient_regis.objects.all()
    ac=phar_regis.objects.all()
    ad=lab_regis.objects.all()
    ba=out_hosptital_regis.objects.all()
    bb=out_phar_regis.objects.all()
    bc=out_lab_regis.objects.all()
    a=aa.count()
    b=ab.count()
    c=ac.count()
    d=ad.count()
    e=ba.count()
    f=bb.count()
    g=bc.count()
    print("aa",a,"ab",b,"ac",c,"ad",d)
    obj=admin_tb.objects.get(lid=1)
    obj.hos=a
    obj.pat=b
    obj.lab=d
    obj.phar=c
    obj.out_hosp=e
    obj.out_phar=f
    obj.out_lab=g
    obj.save()
    if request.session.has_key('uid'):
        data=admin_tb.objects.get(lid=1)
        print (request.session['uid'])
        return render(request,"admin/admin_hm.html",{"data":data})
    
    

#-----------HOSPITAL-------------------------------------------------------------------------------------------------------------------------------

def hm_hosp(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="hospital":
        hos=hosp_regis.objects.get(lid=c)
        dat=hosp_tb.objects.get(lid=c)
        return render(request,"hospital/hospital_hm.html",{"data":hos,"dat":dat})
    else:
        return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
def h_doc(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="hospital":
        hos=hosp_regis.objects.get(lid=c)
        return render(request,"hospital/add_doc_hos.html",{"hos":hos})
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
    
def doc_h_add(request):
    print("doc add")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="hospital":
        a=request.POST.get("name")
        m=request.POST.get("loc")
        n=request.POST.get("dob")
        o=request.POST.get("gender")
        b=request.POST.get("qual")
        c=request.POST.get("dep")
        d=request.POST.get("exp")
        e=request.POST.get("email")
        f=request.POST.get("ph_no")
        g=request.POST.get("uname")
        h=request.POST.get("pass")
        ab=hosp_regis.objects.get(lid=z)
        i=ab.name
        j=ab.place
        p=ab.hid
        print("i",i,"j",j)
        print("a",a,"b",b,"c",c,"D",d,"e",e,"f",f,"g",g,"h",h)
        aa=login_tb.objects.filter(username=g)
        ab=doc_regis.objects.filter(user=g)
        print("aa",aa.count(),"ab",ab.count())
        if(aa.count()>=1 or ab.count()>=1):
            return HttpResponse("<script>alert('Username alraedy taken. choose another');window.location.href='/h_doc/';</script>")
        if aa.count()==0:
            print("ok")
            obj=login_tb(username=g,password=h,usertype="doctor")
            obj.save()
            user=login_tb.objects.get(username=g,password=h)
            l_id=user.lid
            ob=doc_regis(lid=l_id,hid=p,hos=i,name=a,place=m,dob=n,gender=o,qual=b,special=c,exper=d,email=e,phone=f,user=g,passw=h,avail="Not Available")
            ob.save()
            return HttpResponse("<script>alert('Successfully doctor added');window.location.href='/hm_hosp/';</script>")
    return HttpResponse("<script>alert('login');window.location.href='/login/';</script>")

def h_lab(request):
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="hospital":
        hos=hosp_regis.objects.get(lid=z)
        return render(request,"hospital/add_lab_hos.html",{"hos":hos})
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
def ho_lab_add(request):
    print("lab add")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        a=request.POST.get("con_name")
        b=request.POST.get("email")
        c=request.POST.get("ph_no")
        d=request.POST.get("uname")
        e=request.POST.get("pass")
        ab=hosp_regis.objects.get(lid=z)
        i=ab.name
        j=ab.place
        print("i",i,"j",j)
        print("a",a,"b",b,"z",z,"D",d,"e",e)
        aa=login_tb.objects.filter(username=d)
        ab=hos_lab.objects.filter(user=d)
        print("aa",aa.count(),"ab",ab.count())
        if(aa.count()>=1 or ab.count()>=1):
            return HttpResponse("<script>alert('Username alraedy taken. choose another');window.location.href='/h_lab/';</script>")
        if aa.count()==0:
            print("ok")
            obj=login_tb(username=d,password=e,usertype="laboratory")
            obj.save()
            user=login_tb.objects.get(username=d,password=e)
            l_id=user.lid
            ob=hos_lab(lid=l_id,name=i,place=j,cont_name=a,email=b,ph_no=c,user=d,passw=e)
            ob.save()
            return HttpResponse("<script>alert('Successfully Laboratory added');window.location.href='/hm_hosp/';</script>")
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")

def h_pha(request):
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="hospital":
        hos=hosp_regis.objects.get(lid=z)
        return render(request,"hospital/add_pha_hos.html",{"hos":hos})
def pha_h_add(request):
    print("pharmacy add")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        a=request.POST.get("con_name")
        b=request.POST.get("email")
        c=request.POST.get("ph_no")
        d=request.POST.get("uname")
        e=request.POST.get("pass")
        ab=hosp_regis.objects.get(lid=z)
        i=ab.name
        j=ab.place
        k=ab.address
        print("i",i,"j",j)
        print("a",a,"b",b,"z",z,"D",d,"e",e)
        aa=login_tb.objects.filter(username=d)
        ab=hos_lab.objects.filter(user=d)
        print("aa",aa.count(),"ab",ab.count())
        if(aa.count()>=1 or ab.count()>=1):
            return HttpResponse("<script>alert('Username alraedy taken. choose another');window.location.href='/h_pha/';</script>")
        if aa.count()==0:
            print("ok")
            obj=login_tb(username=d,password=e,usertype="pharmacy")
            obj.save()
            user=login_tb.objects.get(username=d,password=e)
            l_id=user.lid
            ob=hos_phar(lid=l_id,name=i,place=j,cont_name=a,email=b,ph_no=c,user=d,passw=e,address=k)
            ob.save()
            return HttpResponse("<script>alert('Successfully Pharmacy added');window.location.href='/hm_hosp/';</script>")
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")

def hos_doc_vw(request):
    print("doc view")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        ob=hosp_regis.objects.get(lid=z)
        print("ob",ob)
        aa=ob.name
        ab=ob.place
        print("aa",aa)
        doctor=doc_regis.objects.filter(hos=aa)
        print("doctor",doctor.count())
        return render(request,"hospital/doc_hos_view.html",{"doctor":doctor,"hos":ob})
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
def del_h_doc(request):
    print("doc delete")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        a=request.POST.get("name")
        b=request.POST.get("qual")
        c=request.POST.get("dep")
        e=request.POST.get("phon")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        h=request.POST.get("out")
        if(h=="out"):
            obj=login_tb.objects.filter(username=f,password=g)
            obj.delete()
            ob=doc_regis.objects.filter(name=a,qual=b,user=f,passw=g)
            ob.delete()
            return HttpResponse("<script>alert('Doctor account Successfully Removed');window.location.href='/hm_hosp/';</script>")
        return HttpResponse("<script>alert('error');window.location.href='/hm_hosp/';</script>")
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")

def hos_lab_vw(request):
    print("lab view")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        ob=hosp_regis.objects.get(lid=z)
        print("ob",ob)
        aa=ob.name
        ab=ob.place
        print("aa",aa)
        lab=hos_lab.objects.filter(name=aa,place=ab)
        return render(request,"hospital/lab_hos_view.html",{"lab":lab,"hos":ob})
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
def del_h_lab(request):
    print("lab delete")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        a=request.POST.get("name")
        b=request.POST.get("phon")
        c=request.POST.get("email")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        h=request.POST.get("out")
        if(h=="out"):
            obj=login_tb.objects.filter(username=f,password=g)
            obj.delete()
            ob=hos_lab.objects.filter(cont_name=a,ph_no=b,user=f,passw=g)
            ob.delete()
            return HttpResponse("<script>alert('Lab Successfully Removed');window.location.href='/hm_hosp/';</script>")
        return HttpResponse("<script>alert('error');window.location.href='/hm_hosp/';</script>")
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")

def hos_phar_vw(request):
    print("pharmacy view")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        ob=hosp_regis.objects.get(lid=z)
        print("ob",ob)
        aa=ob.name
        ab=ob.place
        print("aa",aa)
        pha=hos_phar.objects.filter(name=aa,place=ab)
        return render(request,"hospital/pha_hos_view.html",{"pha":pha,"hos":ob})
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
def del_h_phar(request):
    print("phar delete")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        a=request.POST.get("name")
        b=request.POST.get("phon")
        c=request.POST.get("email")
        f=request.POST.get("uname")
        g=request.POST.get("pass")
        h=request.POST.get("out")
        if(h=="out"):
            obj=login_tb.objects.filter(username=f,password=g)
            obj.delete()
            ob=hos_phar.objects.filter(cont_name=a,ph_no=b,user=f,passw=g)
            ob.delete()
            return HttpResponse("<script>alert('Pharmacy Successfully Removed');window.location.href='/hm_hosp/';</script>")
        return HttpResponse("<script>alert('error');window.location.href='/hm_hosp/';</script>")
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
def edit_hos(request):
    print("hosp profile")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        hosp=hosp_regis.objects.get(lid=z)
        data=login_tb.objects.get(lid=z)
        return render(request,"hospital/edit_prof.html",{"hosp":hosp,"data":data})
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")
def upd_hos(request):
    print("hosp profile")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        a=request.POST.get("cont_name")
        b=request.POST.get("cont_no")
        c=request.POST.get("email")
        d=request.POST.get("pass")
        print("a","b","c","d",a,b,c,d)
        obj=hosp_regis.objects.get(lid=z)
        obj.cont_name=a
        obj.ph_no=b
        obj.email=c
        obj.save()
        ob=login_tb.objects.get(lid=z)
        ob.password=d
        ob.save()
        return HttpResponse("<script>alert('Profile Successfully updated');window.location.href='/hm_hosp/';</script>")
    return HttpResponse("<script>alert('Please login as Hospital');window.location.href='/login/';</script>")

def fresh(request):
    print("refresh")
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        aa=hosp_regis.objects.get(lid=z)
        print(aa.name)
        ab=doc_regis.objects.filter(hos=aa.name)
        ac=hos_phar.objects.filter(name=aa.name)
        ad=hos_lab.objects.filter(name=aa.name)
        a=ab.count()
        b=ac.count()
        c=ad.count()
        print(ab,ac,ad)
        obj=hosp_tb.objects.get(lid=z)
        obj.doc=a
        obj.pha=b
        obj.lab=c
        obj.save()    
    if request.session.has_key('uid'):
        dat=hosp_tb.objects.get(lid=z)
        print (request.session['uid'])
        return render(request,"hospital/hospital_hm.html",{"dat":dat})

def recp(request):
    if request.session.has_key('uid'):
        z=request.session['uid']
        obj=login_tb.objects.filter(lid=z)
        for i in obj:
            typ=i.usertype
    print(typ)
    if request.session.has_key('uid') and typ=="hospital":
        a=request.POST.get("uname")
        b=request.POST.get("pass")
        dat=hosp_regis.objects.get(lid=z)
        amt=login_tb.objects.filter(username=a)
        if(amt.count()==0):
            obj=login_tb(username=a,password=b,usertype="recept")
            obj.save()
            obj=login_tb.objects.get(username=a,password=b)
            data=recep(hos_id=z,hos=dat.name,place=dat.place,lid=obj.lid)
            data.save()
            return HttpResponse("<script>alert('Successfully added');window.location.href='/hm_hosp/';</script>")
        else:
            return HttpResponse("<script>alert('Username Already exist');window.location.href='/hm_hosp/';</script>")

def pbooking(request):
    c=request.session['uid']
    global pat
    print("checkqr")
    val="9"
    s=request.FILES["file"]
    if s:
        fs=  FileSystemStorage("app\\static\\res")
        try:
            os.remove("app\\static\\res\\out.png")
        except:
            pass
        fs.save("out.png",s)
        try:
            img = cv2.imread('app\\static\\res\\out.png')
            d = decode(img)
            val=d[0].data.decode('ascii')
           
        except Exception as e:
            print("cannot read",e)
    print("Value: ",val)
    pat=int(val)
    user=recep.objects.get(lid=c)
    obb=patient_regis.objects.filter(lid=int(val))
    if(obb.count()==0):
        return HttpResponse("<script>alert('No Data Available. check crct qr');window.location.href='/wdept/';</script>")
    else:
        ob=patient_regis.objects.get(lid=int(val))
        obj=recep.objects.get(lid=request.session['uid'])
        from datetime import date
        today = date.today()
    return render(request,"hospital/appoitment.html",{"user":obj,"data":ob,"today":today})
    #return render(request,"hospital/list.html",{"doc":data,"day":today})

def wdept(request):
    return render(request,"hospital/booking.html",{})

def iibook(request):
    m=request.session['uid']
    a=request.POST.get("pid")
    b=request.POST.get("pname")
    c=request.POST.get("selt_hosp")
    d=request.POST.get("departmnt")
    e=request.POST.get("dr")
    g=request.POST.get("tym")
    ob=patient_regis.objects.get(lid=a,name=b)
    aa=recep.objects.get(lid=m)
    data=doc_regis.objects.get(did=e,hos=c,special=d)
    from datetime import date
    today = date.today()
    dates=ob.dob
    ag = int(today.year) - int(dates.year)
    obj=booking_tb(pid=a,did=data.did,location=aa.place,specialization=d,time=g,date=today,hid=data.hid,name=b,age=ag,gender=ob.gender,place=ob.place,hosp_name=c,dr_name=data.name,status="Requested")
    obj.save()
    return HttpResponse("<script>alert('Booked Successful');window.location.href='/wdept/';</script>")

def avail(request):
    print("available")
    a=request.POST.get("loc")
    b=request.POST.get("selt_hosp")
    c=request.POST.get("departmnt")
    d=request.POST.get("dr")
    dc=doc_regis.objects.filter(did=d,hid=b)
    print(a,b,c,d)
    cnt=dc.count()
    from datetime import date
    today = date.today()
    if (cnt==1):
        e=doc_regis.objects.get(did=d,hid=b)
        aa=e.name
        ab=e.hos
        print("doctor")
        data=doc_regis.objects.all().filter(hos=ab,special=c,name=aa)
        return render(request,"hospital/list.html",{"doc":data,"day":today})
    else:
        e=hosp_regis.objects.get(hid=b)
        ab=e.name
        print("no doc")
        data=doc_regis.objects.all().filter(hos=ab,special=c)
        return render(request,"hospital/list.html",{"doc":data,"day":today})
        
    
#--------------DOCTOR----------------------------------------------------------------------------------------------------------------------------

def doct_hm(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="doctor":
        data=doc_regis.objects.get(lid=c)
        print (request.session['uid'])
        return render(request,"doctor/dr_homelog.html",{"user":data})
    else:
        return HttpResponse("<script>alert('Please login using username and password');window.location.href='/login/';</script>")
def dr_bk_vw(request):
    print ("dr bking vw")
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="doctor":
        data=doc_regis.objects.get(lid=c)
        print("ok")
        from datetime import date
        today = date.today()
        print(today)
        book=booking_tb.objects.filter(did=data.did,date=today)
        return render(request,"doctor/Patient_dr_bk_vw.html",{"book":book,"user":data})
    else:
        return HttpResponse("<script>alert('Please login using username and password');window.location.href='/login/';</script>")

def qrcheck_dr(request):
    c=request.session['uid']
    global pat
    print("checkqr")
    val="9"
    s=request.FILES["files"]
    if s:
        fs=  FileSystemStorage("app\\static\\res")
        try:
            os.remove("app\\static\\res\\out.png")
        except:
            pass
        fs.save("out.png",s)
        try:
            img = cv2.imread('app\\static\\res\\out.png')
            d = decode(img)
            val=d[0].data.decode('ascii')
           
        except Exception as e:
            print("cannot read",e)
    print("Value: ",val)
    pat=int(val)
    user=doc_regis.objects.get(lid=c)
    obb=patient_regis.objects.filter(lid=int(val))
    if(obb.count()==0):
        return HttpResponse("<script>alert('No Data Available. check crct qr');window.location.href='/doct_hm/';</script>")
    else:
        ob=patient_regis.objects.get(lid=int(val))
    from datetime import date
    today = date.today()
    ob.date=today
    dates=ob.dob
    ag = int(today.year) - int(dates.year)
    ob.age=ag
    test=lab_tb.objects.all().filter(pid=int(val)).order_by('-date')
    pre=phar_tb.objects.all().filter(pid=int(val)).order_by('-date')
    return render(request,"doctor/qr_pat_page.html",{"data":ob,"user":user,"phar":pre,"lab":test})

def back(request):
    c=request.session['uid']
    user=doc_regis.objects.get(lid=c)
    global pat
    ob=patient_regis.objects.get(lid=int(pat))
    test=lab_tb.objects.all().filter(pid=int(pat)).order_by('-date')
    pre=phar_tb.objects.all().filter(pid=int(pat)).order_by('-date')
    from datetime import date
    today = date.today()
    ob.date=today
    dates=ob.dob
    ag = int(today.year) - int(dates.year)
    ob.age=ag
    return render(request,"doctor/qr_pat_page.html",{"data":ob,"user":user,"phar":pre,"lab":test})

def test_dr(request):
    global pat
    c=request.session['uid']
    a=request.POST.get("test")
    b=request.POST.get("date")
    d=request.POST.get("pid")
    obj=doc_regis.objects.get(lid=c)
    print (pat)
    aa=patient_regis.objects.get(lid=pat)
    ob=lab_tb(name="Not visited",pid=d,test=a,doc=obj.name,hos=obj.hos,date=b,result="default.png",pat=aa.name,
              )
    ob.save()
    return HttpResponse("<script>alert('Test successfully added');window.location.href='/back/';</script>")

def pre_dr(request):
    c=request.session['uid']
    a=request.POST.get("date")
    b=request.POST.get("dis")
    d=request.POST.get("med")
    e=request.POST.get("times")
    f=request.POST.get("day")
    g=request.POST.get("pid")
    obj=doc_regis.objects.get(lid=c)
    global pat
    aa=patient_regis.objects.get(lid=pat)
    ob=phar_tb(name="Not visited",pid=g,date=a,doc=obj.name,hos=obj.hos,disease=b,med=d,timing=e,days=f,pat=aa.name
              )
    ob.save()
    return HttpResponse("<script>alert('Prescription successfully added');window.location.href='/back/';</script>")

def submit(request):
    c=request.session['uid']
    user=doc_regis.objects.get(lid=c)
    d=user.name
    e=user.special
    f=user.hos
    a=request.POST.get("id")
    b=request.POST.get("name")
    from datetime import date
    today = date.today()
    print(today)
    obj=booking_tb.objects.get(pid=a,name=b,specialization=e,dr_name=d,hosp_name=f,date=today)
    obj.status="Visited"
    obj.save()
    return HttpResponse("<script>alert('Consultation Completed');window.location.href='/doct_hm/';</script>")

#--------------PATIENT----------------------------------------------------------------------------------------------------------------------

def pat_hm(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="patient":
        user=patient_regis.objects.get(lid=c)
        print (request.session['uid'])
        return render(request,"patient/patient_hm.html",{"user":user})
    else:
        return HttpResponse("<script>alert('Please login using username and password');window.location.href='/login/';</script>")
def for_log(request):
    return render(request,"patient_log.html",{})
def check_log(request):
    print ("in login_check_after for book appoitment")
    count=0
    if request.method=="POST":
        un=request.POST.get("uname")
        ps=request.POST.get("pass")
        print ("un",un,"ps",ps)
        user=login_tb.objects.filter(username=un,password=ps)
        print (user)
        count=user.count()
        if count==0:
            print ("Invalid User")
            return HttpResponse("<script>alert('Invalid User');window.location.href='/index/';</script>")
        else:
            for i in user:
                typ=i.usertype
                llid=i.lid
            print ("type",typ,"username",un,"paswd",ps,"usercount",count,"userid",llid)
            if count==0 or count>1:
                return render(request,"index.html",{"msg":"Invalid Userdata"})
            if count==1 and typ=="patient":
                print ("patient page")
                user_dt=patient_regis.objects.get(lid=llid)
                request.session['uid']=user_dt.lid
                print ("session=: created ",request.session['uid'])
                print ("user loged in is",request.session['uid'])
                uname=patient_regis.objects.get(lid=request.session['uid'])
                p_nm=uname.name
                global bk_loc,bk_hos,bk_dist,bk_dr,bk_dt,bk_tym
                print ("bk_loc",bk_loc)
                print ("bk_hos",bk_hos)
                print ("bk_dist",bk_dist)
                print ("bk_dr",bk_dr)
                print ("bk_dt",bk_dt)
                print ("bk_tym",bk_tym)
                import datetime
                date_str = bk_dt # The date - 29 Dec 2017
                format_str = '%m/%d/%Y' # The format
                datetime_obj = datetime.datetime.strptime(date_str, format_str)
                print(datetime_obj.date())
                bk_dt=str(datetime_obj.date())
                check_bk=booking_tb.objects.filter(did=bk_dr,date=bk_dt,time=bk_tym)
                print ("no of bookings",check_bk.count())
                if check_bk.count()<=2:
                    print ("check_bk.count()",check_bk.count())
                    hsp=hosp_regis.objects.get(hid=bk_hos)
                    dr=doc_regis.objects.get(did=bk_dr)
                    pat=patient_regis.objects.get(lid=request.session['uid'])
                    gen=pat.gender
                    plc=pat.place
                    from datetime import date
                    today = date.today()
                    dates=pat.dob
                    ag = int(today.year) - int(dates.year)
                    obj=booking_tb(
                        pid=request.session['uid'],did=bk_dr,location=bk_loc,age=ag,place=plc,gender=gen,status="Requested",specialization=bk_dist,time=bk_tym,date=bk_dt,hid=bk_hos,hosp_name=hsp.name,dr_name=dr.name,name=p_nm
                        )
                    obj.save()
                    print ("booked")
                    bk_loc=""
                    bk_hos=""
                    bk_dist=""
                    bk_dr=""
                    bk_dt=""
                    bk_tym=""
                    print ("global deleted")
                    print ("bk_loc",bk_loc)
                    print ("bk_hos",bk_hos)
                    print ("bk_dist",bk_dist)
                    print ("bk_dr",bk_dr)
                    print ("bk_dt",bk_dt)
                    print ("bk_tym",bk_tym)
                    return HttpResponse("<script>alert('Booked Successful');window.location.href='/pat_hm/';</script>")
                else:
                    return HttpResponse("<script>alert('Sorry booking closed for this day');window.location.href='/pat_hm/';</script>")
                
        return render(request,"index.html",{"msg":"Invalid User"})

def vw_dr(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="patient":
        obj=booking_tb.objects.filter(pid=c)
        return render(request,"patient/view_appoinment.html",{"vw":obj})

def pt_test(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="patient":
        lab=lab_tb.objects.all().filter(pid=c).order_by('-date')
        return render(request,"patient/lab_history.html",{"lab":lab})
def pt_pre(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="patient":
        pres=phar_tb.objects.all().filter(pid=c).order_by('-date')
        return render(request,"patient/pres_history.html",{"pres":pres})
    
    

#--------------PHARMACY------------------------------------------------------------------------------------------------------------------------

def pha_hm(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="pharmacy":
        user=hos_phar.objects.get(lid=c)
        return render(request,"pharmacy/phar_hmlog.html",{"user":user})
    else:
        return HttpResponse("<script>alert('Please login using lab username and password');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login using lab username and password');window.location.href='/login/';</script>")

def presc_pha(request):
    c=request.session['uid']
    global pat
    print("checkqr")
    val="9"
    s=request.FILES["files"]
    if s:
        fs=  FileSystemStorage("app\\static\\res")
        try:
            os.remove("app\\static\\res\\out.png")
        except:
            pass
        fs.save("out.png",s)
        try:
            img = cv2.imread('app\\static\\res\\out.png')
            d = decode(img)
            val=d[0].data.decode('ascii')
           
        except Exception as e:
            print("cannot read",e)
    print("Value: ",val)
    pat=int(val)
    user=hos_phar.objects.get(lid=c)
    obb=patient_regis.objects.filter(lid=int(val))
    if(obb.count()==0):
        return HttpResponse("<script>alert('No Data Available. check crct qr');window.location.href='/pha_hm/';</script>")
    else:
        ob=patient_regis.objects.get(lid=int(val))
    from datetime import date
    today = date.today()
    ob.date=today
    dates=ob.dob
    ag = int(today.year) - int(dates.year)
    ob.age=ag
    pre=phar_tb.objects.all().filter(pid=int(val),name="Not visited").order_by('-date')
    return render(request,"pharmacy/qrcode_after.html",{"data":ob,"user":user,"phar":pre})

def pstatus(request):
    c=request.session['uid']
    user=hos_phar.objects.get(lid=c)
    a=request.POST.get("date")
    b=request.POST.get("hos")
    d=request.POST.get("pt")
    e=request.POST.get("doc")
    mm=request.POST.get("med")
    time=request.POST.get("t")
    day=request.POST.get("d")
    f=request.POST.get("llid")
    sums=0
    for i in range (0,5,2):
        sums=sums+int(time[i])
    print(sums)
    s=sums*int(day)
    print(s)
    da=med_stock.objects.filter(med=mm)
    if (da.count()==0):
        return HttpResponse("<script>alert('Medicine not Added');window.location.href='/pg_med_add/';</script>")
    if (da.count()==1):
        st=med_stock.objects.get(med=mm,hos=b)
        aa=st.stock
        new=int(aa)-int(s)
        st.stock=new
        st.save()
        obj=phar_tb.objects.get(pid=d,doc=e,date=a,hos=b,llid=f)
        obj.name=user.name
        obj.save()
    #return render(request,"pharmacy/phar_hmlog.html",{"user":user})
        return HttpResponse("<script>alert('Prescription Successfully Provided');window.location.href='/pha_hm/';</script>")

def vew_presc(request):
    c=request.session['uid']
    user=hos_phar.objects.get(lid=c)
    a=user.name
    print(a)
    from datetime import date
    time=date.today()
    today=time.strftime("%B %d, %Y")
    print(time.strftime("%B %d, %Y"))
    data=phar_tb.objects.all().filter(hos=user.name,name="Not visited",date=today).order_by('-date')
    if(data.count()==0):
        return HttpResponse("<script>alert('No Prescription Request Available');window.location.href='/pha_hm/';</script>")
    return render(request,"pharmacy/pres_view.html",{"user":user,"pres":data})

def me_vw(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="pharmacy":
        user=hos_phar.objects.get(lid=c)
        data=med_stock.objects.filter(hos=user.name,place=user.place).order_by('med')
        return render(request,"pharmacy/view_medicine.html",{"user":user,"data":data})
def pg_med_add(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="pharmacy":
        user=hos_phar.objects.get(lid=c)
        return render(request,"pharmacy/add_med.html",{"user":user})

def stock(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="pharmacy":
        a=request.POST.get("f_date")
        b=request.POST.get("e_date")
        m=request.POST.get("med")
        h=request.POST.get("dis")
        d=request.POST.get("stock")
        ob=hos_phar.objects.get(lid=c)
        e=ob.name
        f=ob.place
        ss=ob.ph_no
        aa=hosp_regis.objects.get(name=e,place=f)
        g=aa.lid
        obj=med_stock(f_date=a,e_date=b,med=m,disease=h,lid=g,stock=d,hos=e,place=f,ph_no=ss)
        obj.save()
        obb=med_stock.objects.get(f_date=a,e_date=b,med=m,disease=h,lid=g,stock=d,hos=e,place=f)
        obb.address=ob.address
        obb.save()
        return HttpResponse("<script>alert('Stock Successfully updated');window.location.href='/pha_hm/';</script>")
def print_bill(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="pharmacy":
        user=phar_tb.objects.get(lid=c)
        return render(request,"pharmacy/bill_pha.html",{"user":user})
def z_stock(request):
    return render(request,"search.php",{})
def medchecker(request):
    a=request.POST.get("loc")
    b=request.POST.get("product")
    print(a,b)
    obj=med_stock.objects.filter(med=b,place=a,stock__gt=50).distinct()
    if obj.count()>=1:
        status="Available"
        return render(request,"med_check.html",{"data":obj,"status":status})
    else:
        return HttpResponse("<script>alert('Medicine not Available Now');window.location.href='/stk_med/';</script>")
        
    
        
#---------------LAB-------------------------------------------------------------------------------------------------------------------------------

def homelab(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="laboratory":
        user=hos_lab.objects.get(lid=c)
        return render(request,"lab/lab_hmlog.html",{"user":user})
    else:
        return HttpResponse("<script>alert('Please login using lab username and password');window.location.href='/login/';</script>")
    return HttpResponse("<script>alert('Please login using lab username and password');window.location.href='/login/';</script>")

def tst_lab(request):
    c=request.session['uid']
    global pat
    print("checkqr")
    val="9"
    s=request.FILES["files"]
    if s:
        fs=  FileSystemStorage("app\\static\\res")
        try:
            os.remove("app\\static\\res\\out.png")
        except:
            pass
        fs.save("out.png",s)
        try:
            img = cv2.imread('app\\static\\res\\out.png')
            d = decode(img)
            val=d[0].data.decode('ascii')
           
        except Exception as e:
            print("cannot read",e)
    print("Value: ",val)
    pat=int(val)
    user=hos_lab.objects.get(lid=c)
    obb=patient_regis.objects.filter(lid=int(val))
    if(obb.count()==0):
        return HttpResponse("<script>alert('No Data Available. check crct qr');window.location.href='/doct_hm/';</script>")
    else:
        ob=patient_regis.objects.get(lid=int(val))
    from datetime import date
    today = date.today()
    ob.date=today
    dates=ob.dob
    ag = int(today.year) - int(dates.year)
    ob.age=ag
    ob.save()
    lab=lab_tb.objects.all().filter(pid=int(val),name="Not visited").order_by('-date')
    return render(request,"lab/qrcode_after_lab.html",{"data":ob,"user":user,"lab":lab})

def lstatus(request):
    c=request.session['uid']
    user=hos_lab.objects.get(lid=c)
    a=request.POST.get("date")
    b=request.POST.get("test")
    d=request.POST.get("pt")
    e=request.POST.get("doc")
    f=request.POST.get("llid")
    obj=lab_tb.objects.get(pid=d,doc=e,date=a,test=b,llid=f)
    obj.name=user.name
    obj.save()
    return render(request,"lab/lab_hmlog.html",{"user":user})

def vow_lab(request):
    c=request.session['uid']
    user=hos_lab.objects.get(lid=c)
    a=user.name
    print(a)
    from datetime import date
    time=date.today()
    today=time.strftime("%B %d, %Y")
    print(time.strftime("%B %d, %Y"))
    data=lab_tb.objects.all().filter(hos=a,name="Not visited",date=today).order_by('-date')
    if(data.count()==0):
        return HttpResponse("<script>alert('No Test Request Available');window.location.href='/homelab/';</script>")
    return render(request,"lab/lab_view.html",{"user":user,"lab":data})

def info(request):
    a=request.POST.get("date")
    b=request.POST.get("test")
    d=request.POST.get("pt")
    e=request.POST.get("doc")
    f=request.POST.get("llid")
    print(a,b,d,e,f)
    obj=lab_tb.objects.get(pid=d,doc=e,date=a,test=b,llid=f)
    return render(request,"lab/upload.html",{"data":obj})

def file_lab(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        print(c)
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="laboratory":
        a=request.POST.get("pid")
        b=request.POST.get("pat")
        user=hos_lab.objects.get(lid=c)
        if request.method=='POST':
            upload_file=request.FILES['document']
            fs=FileSystemStorage()
            obj=lab_tb.objects.get(pid=a,pat=b,name="Not visited")
            obj.result=upload_file
            obj.name=user.name
            obj.save()
            return HttpResponse("<script>alert('Result uploaded successfully');window.location.href='/homelab/';</script>")


    
#-----------------------------------------------Booking------------------------------------------------------------------------------------

def list_hosp(request):
    print ("list_hosp")
    data={}
    loc=request.GET.get("loc")
    print ("District___________________________________________",loc)
    ob=serializers.serialize("json",hosp_regis.objects.filter(place=loc))
    data["dt1"]=json.loads(ob)
    print (data)
    return JsonResponse(data,safe=False)
def list_dept(request):
    print ("list_dept")
    data={}
    hosp_id=request.GET.get("hosp_id")
    print ("hospital id___________________________________________",hosp_id)
    ob=serializers.serialize("json",doc_regis.objects.filter(hid=hosp_id))
    data["dt1"]=json.loads(ob)
    print (data)
    return JsonResponse(data,safe=False)
def list_dr(request):
    print ("list_dr")
    data={}
    dept=request.GET.get("dept")
    hosp_id=request.GET.get("hosp_id")
    print ("selected department id___________________________________________",dept,hosp_id)
    ob=serializers.serialize("json",doc_regis.objects.filter(special=dept,hid=hosp_id))
    data["dt1"]=json.loads(ob)
    print (data)
    return JsonResponse(data,safe=False)
def nn_list_dr(request):
    print ("list_dr")
    data={}
    dept=request.GET.get("dept")
    ho=recep.objects.get(lid=request.session['uid'])
    aa=ho.hos
    ab=ho.place
    hos_id=hosp_regis.objects.get(name=aa,place=ab)
    print ("selected department id___________________________________________",dept)
    ob=serializers.serialize("json",doc_regis.objects.filter(special=dept,hid=hos_id.hid))
    data["dt1"]=json.loads(ob)
    print (data)
    return JsonResponse(data,safe=False)
def pt_hm_book(request):
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.session.has_key('uid') and typ=="patient":
        return render(request,"patient/book_appoinment.html",{})
        
def book_now(request):
    print ("in book_now page fn when user not login in")
    global bk_loc,bk_hos,bk_dist,bk_dr,bk_dt,bk_tym
    if request.session.has_key('uid'):
        c=request.session['uid']
        obj=login_tb.objects.filter(lid=c)
        for i in obj:
            typ=i.usertype
    if request.method=="POST":
        if request.session.has_key('uid') and typ=="patient":
            user_dt=patient_regis.objects.get(lid=request.session['uid'])
            print ("user loged in is",request.session['uid'])
            uname=patient_regis.objects.get(lid=request.session['uid'])
            p_nm=uname.name
            print ("p_nm",p_nm)
            bk_loc=request.POST.get("loc")
            bk_hos=request.POST.get("selt_hosp")
            bk_dist=request.POST.get("departmnt")
            bk_dr=request.POST.get("dr")
            bk_dt=request.POST.get("appointment_dt")
            bk_tym=request.POST.get("appoint_tym")
            print ("bk_loc",bk_loc)
            print ("bk_hos",bk_hos)
            print ("bk_dist",bk_dist)
            print ("bk_dr",bk_dr)
            print ("bk_dt",bk_dt)
            print ("bk_tym",bk_tym)
            import datetime
            date_str = bk_dt # The date - 29 Dec 2017
            format_str = '%m/%d/%Y' # The format
            datetime_obj = datetime.datetime.strptime(date_str, format_str)
            print(datetime_obj.date())
            bk_dt=str(datetime_obj.date())
            check_bk=booking_tb.objects.filter(did=bk_dr,date=bk_dt,time=bk_tym)
            print ("no of bookings",check_bk.count())
            if check_bk.count()<=2:
                hsp=hosp_regis.objects.get(hid=bk_hos)
                dr=doc_regis.objects.get(did=bk_dr)
                pat=patient_regis.objects.get(lid=request.session['uid'])
                gen=pat.gender
                plc=pat.place
                from datetime import date
                today = date.today()
                dates=pat.dob
                ag = int(today.year) - int(dates.year)
                obj=booking_tb(
                    pid=request.session['uid'],did=bk_dr,location=bk_loc,age=ag,place=plc,gender=gen,status="Requested",specialization=bk_dist,time=bk_tym,date=bk_dt,hid=bk_hos,hosp_name=hsp.name,dr_name=dr.name,name=p_nm
                    )
                obj.save()
                print ("booked")
                msgg="booked"
                llid=request.session['uid']
                return HttpResponse("<script>alert('Booked Successful');window.location.href='/pat_hm/';</script>")
            else:
                return HttpResponse("<script>alert('Sorry booking closed for this day');window.location.href='/login/';</script>")
                           
        else:
            bk_loc=request.POST.get("loc")
            bk_hos=request.POST.get("selt_hosp")
            bk_dist=request.POST.get("departmnt")
            bk_dr=request.POST.get("dr")
            bk_dt=request.POST.get("appointment_dt")
            bk_tym=request.POST.get("appoint_tym")
            print ("bk_loc",bk_loc)
            print ("bk_hos",bk_hos)
            print ("bk_dist",bk_dist)
            print ("bk_dr",bk_dr)
            print ("bk_dt",bk_dt)
            print ("bk_tym",bk_tym)
            return HttpResponse("<script>alert('Please Login');window.location.href='/for_log/';</script>")
    return render(request,"index.html",{})

def autocomplete(request):
    if 'term' in request.GET:
        print(request.GET.get('term'))
        qs = med_stock.objects.filter(med__istartswith=request.GET.get('term'))
        titles = list()
        for medicine in qs:
            titles.append(medicine.med)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request, 'med_check.html')


