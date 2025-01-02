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
    
