from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, request
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from .forms import PatientSignUpForm,LoginForm
from .models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def account_option(request):
    return render(request,'English/account/account_option.html')

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'templates/English/account/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        email=form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return render(request, 'templates/English/account/signup.html', {'form': form})
        else:
            user = form.save()
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')

            #login(self.request, user)
            '''
            send_mail(
                'Fayyaan Faaya Medical Consultation',
                'Hello, ' + username + ' You are successfully registered and create \n patient account to our website.',
                'fayyaanfaaya@gmail.com',
                [email],
                fail_silently=False,
                )
            '''
            return redirect('login')
    
def doctor_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            send_mail(
                'Fayyaan Faaya Medical Consultation',
                'Hello, Doctor ' + ' Your are registered to Fayyaan Faaya medical consultation in role of doctor\n'+ 
                'your username is ' + username + 'To login please first reset your password!',
                'fayyaanfaaya@gmail.com',
            [email],
            fail_silently=False,
            )

            form.save()
            user = authenticate(username=username, password=password)

            login(request, user)

    else:
        form = UserCreationForm()
    return render(request, 'templates/English/account/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated and request.user.is_patient:
        return redirect('index')
    if request.user.is_authenticated and request.user.is_doctor:
        return redirect('dashboard')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username ,password=password)
        if user is not None:
            if user.is_patient:
                login(request,user)
                return redirect('index')
            elif user.is_doctor:
                login(request,user)
                return redirect('dashboard')  
            elif user.is_superuser:
                return redirect('admin:index')
        else:
            messages.error(request,"Please enter correct username & password")

       return render(request, 'English/account/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
