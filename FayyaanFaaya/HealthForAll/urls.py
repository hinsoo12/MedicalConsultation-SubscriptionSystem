from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('subscriber/', views.subscriber, name='subscriber'),
    path('news/', views.news, name='news'),
    path('checkdisease/', views.checkdisease, name='checkdisease'),
    path('diseaseinfo/',views.diseaseinfo, name='diseaseinfo'),
    path('consult_option/', views.consult_option, name='consult_option'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('notfound/', views.notfound, name='notfound'),

    # Urls of disease information

    path('cancer/', views.cancer, name='cancer'),


]