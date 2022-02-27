from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

admin.site.site_header = 'Fayyaan Faaya Login Page'
admin.site.site_title = 'Fayyaan Faaya'
admin.site.index_title = 'Admin Dashboard'


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('HealthForAll.urls')),
    path('Afaan-Oromoo/', include('FayyaanHundaaf.urls')),
    path('Accounts/', include('Accounts.urls')),
    path('Doctors/', include('Doctors.urls')),
    path('Chatbot/', include('Chatbot.urls')),
]
