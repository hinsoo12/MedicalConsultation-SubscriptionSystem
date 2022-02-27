from django.urls import path
from .import views

urlpatterns = [
    path('wiirtuu/',views.wiirtuu,name='wiirtuu'),
    path('waahee/', views.waahee, name='waahee'),
    path('quunnamti/', views.quunnamti, name='quunnamti'),
    path('waahee/', views.waahee, name='waahee'),
    
    path('Afaan-Oromoo/kalee', views.kalee, name='kalee'),
    path('Afaan-Oromoo/kintaarotii', views.kintaarotii, name='kintaarotii'),

    path('notfound/', views.notfound, name='notfound'),
]