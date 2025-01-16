from django.db import models

# Create your models here.


class Customer(models.Model):
    name=models.TextField()
    email=models.TextField()
    password=models.TextField()

class Catering(models.Model):
    foods=models.TextField()
    price=models.IntegerField()
    dis=models.TextField()

class Decorations(models.Model):
    img1=models.FileField()
    img2=models.FileField()
    img3=models.FileField()
    dis=models.TextField()
    price=models.IntegerField()

class Halls(models.Model):
    image1=models.FileField()
    image2=models.FileField()
    image3=models.FileField()
    name=models.TextField()
    dis=models.TextField()
    price=models.IntegerField()

class Camera(models.Model):
    photo=models.BooleanField()
    video=models.BooleanField()
    both=models.BooleanField()
    price=models.IntegerField()


class Staff(models.Model):
    name=models.TextField()
    email=models.TextField()
    password=models.TextField()
    phone=models.IntegerField()
    status=models.TextField()
    catering=models.ForeignKey(Catering,on_delete=models.CASCADE,null=True)
    decoration=models.ForeignKey(Decorations,on_delete=models.CASCADE,null=True)
    photography=models.ForeignKey(Camera,on_delete=models.CASCADE,null=True)

class Contact(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    phone=models.IntegerField()
    message=models.TextField(null=True)
    review=models.TextField(null=True)

class Bookings(models.Model):
    hall=models.ForeignKey(Halls,on_delete=models.CASCADE,null=True)
    bookingdate=models.DateField(null=True)
    
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    total_price=models.IntegerField()
    phone=models.IntegerField()

class DecBookings(models.Model):
    decoration=models.ForeignKey(Decorations,on_delete=models.CASCADE,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    address=models.TextField(null=True)
    phone=models.IntegerField()
    total_price=models.IntegerField()
    bookingdate=models.DateField(null=True)

class FoodBooking(models.Model):
    foods = models.ManyToManyField(Catering) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2) 
    booking_date = models.DateField(null=True)
    time = models.TimeField()
    address = models.TextField(null=True)
    phone = models.IntegerField()
    qty=models.IntegerField()

    def __str__(self):
        return f"Booking for {self.customer.name} on {self.booking_date}"

class PurchaseHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    hall_name = models.CharField(max_length=255, null=True, blank=True)
    decoration_name = models.CharField(max_length=255, null=True, blank=True)
    food_items = models.TextField(null=True, blank=True)  # Store food names as a comma-separated string
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField(auto_now_add=True)
    purchase_time = models.TimeField(auto_now_add=True)
    address = models.TextField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)










    






    
