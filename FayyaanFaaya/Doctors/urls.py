from django.urls import path
from .import views

urlpatterns = [
     path('doctor/dashboard/',views.dashboard,name="dashboard"),
     path('dnews/',views.dnews, name='dnews'),
     path('doctor/addinfo/',views.addinfo,name="addinfo"),

]

