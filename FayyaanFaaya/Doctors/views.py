from django.shortcuts import redirect, render
from django.contrib.auth import logout
from HealthForAll.models import DiseaseInfo, subscribe,News
from django.core.mail import send_mail
from django.contrib import messages

def dashboard(request):
    subscriber = subscribe.objects.all()
    return render(request,'English/doctor/dashboard.html',{'subscriber':subscriber})

def addinfo(request):
    if request.method == 'POST':
        diseasename = request.POST['disease']
        diseasedescription = request.POST['description']
        diseasesymptom = request.POST['symptoms']
        diseasetreatment = request.POST['treatment']

        if len(diseasename)<2 or len(diseasedescription)<5 or len(diseasesymptom)<4 or len(diseasetreatment)<4:
              messages.error(request, "Please add all required information correctly")
        else:
            reciever = subscribe.objects.all()
            send_mail(
                'Fayyaan Faaya Medical Consultation',
                diseasename + diseasedescription + diseasesymptom + diseasetreatment,
                'fayyaanfaaya@gmail.com',
                [reciever],
                fail_silently=False,
                )

            disease=DiseaseInfo(diseasename = diseasename, diseasedescription = diseasedescription, diseasesymptom = diseasesymptom, diseasetreatment = diseasetreatment)
            disease.save()

            messages.info(request,'You successfully add health info')
            messages.info(request,'Your added information is accessed by subscribers.')
            return redirect('dashboad')
    return render(request,'English/doctor/addinfo.html')


def dnews(request):
    news = News.objects.all()
    return render(request,'English/doctor/dnews.html',{'news':news})
    