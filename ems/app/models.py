from django.db import models

# Create your models here.
class Staff(models.Model):
    name=models.TextField()
    email=models.TextField()
    password=models.TextField()
    phone=models.IntegerField()

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



    






    
