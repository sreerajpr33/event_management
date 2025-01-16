from django.shortcuts import render,redirect
from . models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import re
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User,auth
from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.http import JsonResponse
from datetime import date
from datetime import datetime
from django.db import transaction
from django.utils.timezone import now


# login and reg.


# def login(req):
#     return render(req,'login.html')




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
    

def adm_halls(req):
    if 'admin'in req.session:
        if req.method=='POST':
            img1=req.FILES['image1']
            img2=req.FILES['image2']
            img3=req.FILES['image3']
            name=req.POST['hallName']
            dis=req.POST['description']
            price=req.POST['price']
            data=Halls.objects.create(image1=img1,image2=img2,image3=img3,name=name,dis=dis,price=price)
            data.save()
        datas=Halls.objects.all()
        return render(req,'admin/admin_halls.html',{'halls':datas})
    else:
        return redirect(login)
    
def adm_photo(req):
    if 'admin' in req.session:
        return render(req,'admin/photography.html')
    else:
        return redirect(login)
    
def adm_bookings(req):
    if 'admin'in req.session:
        bookings=PurchaseHistory.objects.all()
        return render(req,'admin/viewbooking.html',{'bookings':bookings})
    else:
        return redirect(login)


# user
def user_home(req):
    if 'user' in req.session:
        data=Halls.objects.all()[::-1][:3]
        datas=Decorations.objects.all()[::-1][:3]
        return render(req,'user/user_home.html',{'halls':data,'decorations':datas})
    else:
        return redirect(login)
    
def user_about(req):
    if 'user' in req.session:
        data=Contact.objects.all()[::-1]
        return render(req,'user/about.html',{'reviews':data})
    else:
        return redirect(login)

def user_contact(req):
    if 'user' in req.session:
        user = Customer.objects.get(email=req.session['user'])

        if req.method == 'POST':
            phone = req.POST['phone']   
            review = req.POST['review']   
            data=Contact.objects.create(customer=user,phone=phone,review=review)
            data.save()
        return render(req, 'user/contact.html', {'user': user})
    else:
        return redirect(login)
    
def profile(req):
    if 'user' in req.session:
        user = Customer.objects.get(email=req.session['user'])
        data=Contact.objects.get(customer=user)
        return render(req,'user/profile.html',{'user':data})
    else:
        return redirect(login)
    
def edit_profile(req, cid):
    if 'user' in req.session:
        contact = Contact.objects.get(pk=cid) 

        if req.method == 'POST':

            contact.phone = req.POST.get('phone', contact.phone)
            contact.message = req.POST.get('address', contact.message)
            contact.save() 

            return redirect('profile') 


        return render(req, 'user/edit_profile.html', {'contact': contact})
    
    else:
        return redirect('login')
    
def halldetails(req,pid):
    if 'user' in req.session:
        data=Halls.objects.get(pk=pid)
        return render(req,'user/halldetails.html',{'service':data})
    else:
        return redirect(login)

def allhalls(req):
    if 'user' in req.session:
        data=Halls.objects.all()
        return render(req,'user/allhalls.html',{'halls':data})
    else:
        return redirect(login)
    
def alldec(req):
    if 'user' in req.session:
        data=Decorations.objects.all()
        return render(req,'user/alldec.html',{'decorations':data})
    else:
        return redirect(login)
    
def dec_details(req, pid):
    if 'user' in req.session:
        data = Decorations.objects.get(pk=pid)  # Get decoration details
        foods = Catering.objects.all()  # Fetch all food options

        if req.method == 'POST':
            # Extract form data
            phone = req.POST.get('phone')
            booking_date = req.POST.get('bookingDate')
            address = req.POST.get('address')
            selected_food_id = req.POST.get('selected_food')  # Food selection

            # Retrieve the food item
            selected_food = Catering.objects.get(pk=selected_food_id)

            # Calculate total price
            total_price = data.price + selected_food.price

            # Get the logged-in customer
            customer = Customer.objects.get(user=req.session['user'])

            # Save booking to the database
            booking = Bookings.objects.create(
                hall=None,  # Assuming hall selection is separate
                bookingdate=booking_date,
                address=address,
                customer=customer,
                decoration=data,
                food=selected_food,
                total_price=total_price,
                phone=phone
            )
            booking.save()

            return redirect('success_page')  # Redirect after saving the booking

        return render(req, 'user/decdetails.html', {'service': data, 'foods': foods})
    else:
        return redirect('login')
    






def allfoods(req):
    if 'user' in req.session:
        if req.method == 'POST':
            selected_foods = req.POST.getlist('food[]')  # List of selected food IDs
            quantities = {food_id: int(req.POST.get(f'quantity_{food_id}', 1)) for food_id in selected_foods}  # Get quantities for each selected food
            
            # Get the corresponding food items from the database
            foods = Catering.objects.filter(id__in=selected_foods)
            
            user = Customer.objects.get(email=req.session['user'])
            
            # Calculate total price by multiplying food price with quantity
            total_price = sum(food.price * quantities[str(food.id)] for food in foods)
            
            # Calculate the total quantity
            total_qty = sum(quantities[str(food.id)] for food in foods)
            
            # Remove the commas that make them tuples
            booking_date = req.POST['bookingDate']
            time = req.POST['time']
            address = req.POST['address']
            phone = req.POST['phone']
            
            # Convert string to datetime objects
            date = datetime.fromisoformat(booking_date)
            times = datetime.strptime(time, "%H:%M").time()  # Convert time string to a time object
            
            # Create a new booking
            booking = FoodBooking.objects.create(
                customer=user,
                total_price=total_price,
                booking_date=date,
                time=times,
                address=address,
                phone=phone,
                qty=total_qty  # Store the total quantity
            )
            
            # Save the booking to the database
            booking.save()
            
            # Redirect to a confirmation or success page
            return redirect(buy)  # Replace 'buy' with the actual URL name
        
        else:
            # Retrieve all available foods
            foods = Catering.objects.all()
            return render(req, 'user/allFoods.html', {'services': foods})
    else:
        return redirect('login')  # Ensure the 'login' view name is correct


def bookmark(req, pid):
    if 'user' in req.session:
        data = Halls.objects.get(pk=pid)  # Get the hall object by ID
        user = Customer.objects.get(email=req.session['user'])  # Get the customer based on session email

        if req.method == 'POST':
            number = req.POST.get('phoneNumber')
            date = req.POST.get('bookingDate')
            price = data.price

            # Check if the hall is already booked for the given date
            if PurchaseHistory.objects.filter(hall_name=data.name, purchase_date=date).exists():
                # If a booking exists with the same hall name and date, show an error message
                error_message = "The hall is already booked for this date. Please choose another date."
                return render(req, 'user/bookmark.html', {'service': data, 'error_message': error_message})

            # Proceed to create a booking if the hall is not booked
            bookings = Bookings.objects.create(
                hall=data,
                bookingdate=date,
                phone=number,
                customer=user,
                total_price=price
            )
            bookings.save()
            return redirect(alldec)  # Redirect after booking is successful

        return render(req, 'user/bookmark.html', {'service': data})
    else:
        return redirect(login)


        

    
def dec_mark(req,pid):
    if 'user' in req.session:
        data=Decorations.objects.get(pk=pid)
        user = Customer.objects.get(email=req.session['user'])
        if req.method == 'POST':
            number = req.POST.get('phoneNumber')
            date = req.POST.get('bookingDate')
            address=req.POST.get('address')
            price = data.price
            bookings=DecBookings.objects.create(decoration=data,bookingdate=date,address=address,phone=number,total_price=price,customer=user)
            bookings.save()
            return redirect(allfoods)
        return render(req,'user/dec_mark.html',{'service':data})
    else:
        return redirect(login)
    


def buy(req):
    if 'user' in req.session:
        user = Customer.objects.get(email=req.session['user'])
        
        # Fetch the last added booking for each type
        latest_hall = Bookings.objects.filter(customer=user).order_by('-id').first() if Bookings.objects.filter(customer=user).exists() else None
        latest_decoration = DecBookings.objects.filter(customer=user).order_by('-id').first() if DecBookings.objects.filter(customer=user).exists() else None
        latest_food = FoodBooking.objects.filter(customer=user).order_by('-id').first() if FoodBooking.objects.filter(customer=user).exists() else None
        
        # Calculate total prices using only the last added bookings
        halls_total = latest_hall.total_price if latest_hall else 0
        dec_total = latest_decoration.total_price if latest_decoration else 0
        food_total = latest_food.total_price if latest_food else 0

        # Debugging: print out the totals for each category
        print(f"Last Added Hall Total: {halls_total}")
        print(f"Last Added Decoration Total: {dec_total}")
        print(f"Last Added Food Total: {food_total}")
        
        # Calculate grand total from the last added prices only
        grand_total = halls_total + dec_total + food_total
        
        # Debugging: print the calculated grand total
        print(f"Calculated Grand Total: {grand_total}")
        
        # Pass all data to the template
        context = {
            'halls': latest_hall,  # Passing only the last added hall booking
            'dec': latest_decoration,  # Passing only the last added decoration booking
            'food': latest_food,  # Passing only the last added food booking
            'grand_total': grand_total,
            'latest_hall': latest_hall,
            'latest_decoration': latest_decoration,
            'latest_food': latest_food,
        }
        
        return render(req, 'user/buy.html', context)
    else:
        return redirect('login')  # Ensure 'login' is correctly referenced as the view name

def delete_booking(req, booking_id):
    
    return redirect('your_booking_page')

def delete_hall_booking(req, booking_id):
    if 'user' in req.session:
        user = Customer.objects.get(email=req.session['user'])
        booking = get_object_or_404(Bookings, id=booking_id, customer=user)
        booking.delete()
        return redirect(buy)  # Replace with the correct URL name for the booking page
    else:
        return redirect(login)

# View to delete a decoration booking
def delete_dec_booking(req, booking_id):
    if 'user' in req.session:
        user = Customer.objects.get(email=req.session['user'])
        booking = get_object_or_404(DecBookings, id=booking_id, customer=user)
        booking.delete()
        return redirect(buy)  # Replace with the correct URL name for the booking page
    else:
        return redirect(login)

# View to delete a food booking
def delete_food_booking(req, booking_id):
    if 'user' in req.session:
        user = Customer.objects.get(email=req.session['user'])
        booking = get_object_or_404(FoodBooking, id=booking_id, customer=user)
        booking.delete()
        return redirect(buy)  # Replace with the correct URL name for the booking page
    else:
        return redirect(login)

# staff
def staff_home(req):
    return render(req,'staff/staff_home.html')

def buynow(req):
    if 'user' in req.session:
        user = Customer.objects.get(email=req.session['user'])
        
        # Fetch the latest bookings for each type
        latest_hall = Bookings.objects.filter(customer=user).order_by('-id').first()
        latest_decoration = DecBookings.objects.filter(customer=user).order_by('-id').first()
        latest_food = FoodBooking.objects.filter(customer=user).order_by('-id').first()
        
        # Calculate the total prices
        halls_total = latest_hall.total_price if latest_hall else 0
        dec_total = latest_decoration.total_price if latest_decoration else 0
        food_total = latest_food.total_price if latest_food else 0
        grand_total = halls_total + dec_total + food_total

        # Consolidate food item names
        food_items = (
            ", ".join([food.name for food in latest_food.foods.all()])
            if latest_food else ""
        )
        
        # Address and phone details
        address = latest_decoration.address if latest_decoration else latest_food.address if latest_food else None
        phone = latest_decoration.phone if latest_decoration else latest_food.phone if latest_food else None

        # Save the consolidated data in the new model
        with transaction.atomic():
            PurchaseHistory.objects.create(
                customer=user,
                hall_name=latest_hall.hall.name if latest_hall else None,
                decoration_name=latest_decoration.decoration.dis if latest_decoration else None,
                food_items=food_items,
                grand_total=grand_total,
                address=address,
                phone=phone,
            )

            # Clear the existing bookings
            if latest_hall:
                latest_hall.delete()
            if latest_decoration:
                latest_decoration.delete()
            if latest_food:
                latest_food.delete()
        
        return render(req, 'user/success.html', {'grand_total': grand_total})
    else:
        return redirect('login')

def all_bookings(req):
    if 'user' in req.session:  # Check if the user is logged in
        try:
            user = Customer.objects.get(email=req.session['user'])

            # Fetch all bookings for the logged-in user
            bookings = PurchaseHistory.objects.filter(customer=user).order_by('-id')

            context = {
                'bookings': bookings,  # Pass all bookings to the template
            }
            return render(req, 'user/allbookings.html', context)

        except Customer.DoesNotExist:
            return redirect('login')  # Redirect to login if customer not found
    else:
        return redirect('login')  # Redirect to login if not logged in
    


