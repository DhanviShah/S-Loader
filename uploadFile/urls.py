from django.urls import path

from . import views


urlpatterns = [
    #path('',views.home, name='home'),
    path('',views.index, name='index'),
    path('about',views.about, name='about'),
    path('datamonitor',views.datamonitor, name='datamonitor'),
#basic_form.html
 
]