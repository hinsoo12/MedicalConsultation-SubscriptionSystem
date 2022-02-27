from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields import EmailField
from django.db.models.fields.related import ForeignKey, OneToOneField
from Accounts.models import User, Patient, Doctor

class Our_Service:
    id : int
    service_name : str 

class News(models.Model):
    adder = models.ForeignKey(User,on_delete=models.CASCADE, related_name="Doc")
    title = models.CharField(max_length=200)
    content = models.TextField()

class DiseaseInfo(models.Model):
    adder_doctor = models.ManyToManyField(Doctor,primary_key=False, related_name="adder") 
    diseasename = models.CharField(max_length = 200)
    diseasedescription = models.TextField()
    diseasesymptom =models.TextField()
    diseasetreatment = models.CharField(max_length=250)

class Disease(models.Model):
    diseasename = models.CharField(max_length = 200)
    diseasedescription = models.TextField()
    diseasesymptom =models.TextField()
    diseasetreatment = models.CharField(max_length=250)

class Consultation(models.Model):
    patient = models.ForeignKey(Patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor ,null=True, on_delete=models.SET_NULL)
    consultation_date = models.DateField()
    status = models.CharField(max_length = 20)

class subscribe(models.Model):
    viewer = models.ManyToManyField(User,primary_key=False,related_name="viewer")
    subscriber = models.EmailField(max_length=250)
    subscribe_date = models.DateField("Subscribe date",auto_now= True)

class Feedback(models.Model):
    recieved = models.ManyToManyField(User,primary_key=False)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return "Message from " + self.fullname + ' - ' + self.email

