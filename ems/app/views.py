from django.shortcuts import render,redirect
from . models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import re
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User,auth


# login and reg.


def login(req):
    return render(req,'login.html')




def user_reg(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['Email']
        password5=req.POST['password']
         # Validate email
        try:
            validate_email(email2)
        except ValidationError:
            messages.warning(req, "Invalid email format, please enter a valid email.")
            return render(req, 'register.html')

        # Validate phone number (assuming 10-digit numeric format)
        # try:
        data=Customer.objects.create(name=name1,email=email2,password=password5)
        data.save()
        subject = 'Registration details'
        message = '{} Welcome to Eventease,'.format(name1)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email2]
        send_mail(subject, message, from_email, recipient_list,fail_silently=False)  
        # messages.warning(req, "Email Already Exits , Try Another Email.")
        return redirect(login)
        # except:
    return render(req,'register.html')

def staff_reg(req):
    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['email']
        phonenumber3=req.POST['phonenumber']
        password5=req.POST['password']
        try:
            data=Staff.objects.create(name=name1,email=email2,phone=phonenumber3,password=password5)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'staff/staff_reg.html')



def login(req):
    if 'user' in req.session:
        return redirect(user_home)
    if 'admin' in req.session:
        return redirect(adm_home)
    if 'staff' in req.session:
        return redirect(staff_home)
    if req.method=='POST':
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=Customer.objects.get(email=email,password=password)
            req.session['user']=data.email
            return redirect(user_home)
        except Customer.DoesNotExist:
            admin=auth.authenticate(username=email,password=password)
            if admin is not None:
                auth.login(req,admin)
                req.session['admin']=email

                return redirect(adm_home)
            
            else:
                try:
                    data=Staff.objects.get(email=email,password=password)
                    req.session['staff']=data.email

                    return redirect(staff_home)
                except Staff.DoesNotExist:


                    messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')

def logout(req):
    if 'user' in req.session:
        # req.session.flush()
        del req.session['user']
    if 'admin' in req.session:
        del req.session['admin']
    if 'staff' in req.session:
        del req.session['staff']
    return redirect(login)


#admin
def adm_home(req):
    if 'admin' in req.session:
        return render(req,'admin/admin_home.html')
    else:
        return redirect(login)

def adm_catering(req):
    if 'admin' in req.session:
        if req.method=='POST':
            food=req.POST['food']
            dis=req.POST['dis']
            price=req.POST['price']
            food=food.lower()
            try:
                datas=Catering.objects.get(foods=food)
            except:
                data=Catering.objects.create(foods=food,dis=dis,price=price)
                data.save()
        foods=Catering.objects.all()
        return render(req,'admin/cattering.html',{'foods':foods})
    else:
        return redirect(login)
    
def adm_decr(req):
    if 'admin' in req.session:
        if req.method=='POST':
            img1=req.FILES['image1']
            img2=req.FILES['image2']
            img3=req.FILES['image3']
            dis=req.POST['description']
            price=req.POST['price']
            data=Decorations.objects.create(img1=img1,img2=img2,img3=img3,dis=dis,price=price)
            data.save()
        datas=Decorations.objects.all()
        return render(req,'admin/decorations.html',{'decorations':datas})
    else:
        return redirect(login)




# user
def user_home(req):
    return render(req,'user/user_home.html')

# staff
def staff_home(req):
    return render(req,'staff/staff_home.html')