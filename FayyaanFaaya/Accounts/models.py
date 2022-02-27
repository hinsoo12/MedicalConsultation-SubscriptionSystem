from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    
class SystemAdmin(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name = "related to User", primary_key=True, related_name='admin')

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name = "related to User", primary_key=True, related_name='patient')
    phone_number = models.CharField(max_length=12,null=False, blank=False, unique=True)
    address = models.CharField(max_length=250)

    def __str__(self):
    	return self.user.username

class Doctor(models.Model):
    department = (
        ("Doctor Allergist","Allergist"),("Doctor of Cardiologist","Cardiologist"),("Doctor of Dermatologist","Dermatologist"),("Doctor of Gastroenterologist","Gastroenterologist"),
        ("Doctor of Neurologist","Neurologist"),("Doctor of Orthopedist","Orthopedist"),("Doctor of Rheumatologist","Rheumatologist"),("Doctor of Urologist","Urologist"),("Other","Other")
    )
    social_media = (
        ("Facebook","Facebook"),("Whatsapp","Whatsapp"),("Viber","Viber"),("Telegram","Telegram"),("Other","Other")
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE, verbose_name = "related to User", related_name="doctor", primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=12,null=False, blank=False, unique=True)
    specialization = models.CharField(max_length=100,choices = department)
    address = models.CharField(max_length=250)
    social_media = models.CharField(max_length=200,choices = social_media)
    media_url = models.CharField(max_length=250)
    def __str__(self):
    	return self.user.username 