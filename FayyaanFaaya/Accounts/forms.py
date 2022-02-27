from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import widgets
from phonenumber_field.modelfields import PhoneNumberField

from .models import Patient, User, Doctor

class LoginForm(UserCreationForm):
    username = forms.CharField(widget= forms.TextInput(attrs={ "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email=forms.EmailField(required=True)
    phone_number  = forms.CharField(required=True)
    address = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("The email you enter is already registered!")
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super(PatientSignUpForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user=user)
        patient.phone_number=self.cleaned_data.get('phone_number')
        patient.address=self.cleaned_data.get("address")
        patient.save()
        return patient

class DoctorSignUpForm(UserCreationForm):
    department = (
        ("DocA","Allergist"),("DocC","Cardiologist"),("DocD","Dermatologist"),("DocG","Gastroenterologist"),
        ("DocN","Neurologist"),("DocO","Orthopedist"),("DocR","Rheumatologist"),("DocU","Urologist")
    )
    social_media = (
        ("Facebook","Facebook"),("Whatsapp","Whatsapp"),("Viber","Viber"),("Telegram","Telegram"),("Other","Other")
    )

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email=forms.EmailField(required=True)
    phone_number  = forms.CharField(required=True)
    specialization=forms.CharField(required=True)
    specialization=forms.ChoiceField(choices=department,required=True)
    address=forms.CharField(required=True)
    social_media = forms.ChoiceField(choices=social_media, required=True)
  
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email']
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("The email you enter is already registered!")
        return email
        
    @transaction.atomic
    def save(self, commit=True):
        user = super(PatientSignUpForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_doctor = True
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.phone_number=self.cleaned_data.get('phone_number')
        doctor.specialization=self.cleaned_data.get('specialization')
        doctor.address=self.cleaned_data.get("address")
        doctor.save()
        return doctor