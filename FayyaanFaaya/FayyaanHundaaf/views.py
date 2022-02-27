from django.shortcuts import render

# Create your views here.

def wiirtuu(request):
    return render(request, 'Afaan-Oromoo/fayyaa/wiirtuu.html')

def waahee(request):
    return render(request, 'Afaan-Oromoo/fayyaa/waahee.html')

def quunnamti(request):
    return render(request, 'Afaan-Oromoo/fayyaa/quunnamti.html')

def kalee(request):
    return render(request, 'Afaan-Oromoo/dhibee/kalee.html')

def kintaarotii(request):
    return render(request, 'Afaan-Oromoo/dhibee/kintaarotii.html')

def notfound(request):
    return render(request, 'English/base/404.html')


