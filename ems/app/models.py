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

    







    






    
