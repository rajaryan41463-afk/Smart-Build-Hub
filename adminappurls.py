from django.urls import path
from . import views
urlpatterns = [

    path('admindash/',views.admindash,name='admindash'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('viewenq/',views.viewenq,name='viewenq'),
    path('delenq/<id>',views.delenq,name='delenq'),
    path('fpassword/',views.fpassword,name='fpassword'),
    path('managehomeowners/',views.managehomeowners,name='managehomeowners'),
    path('managecontractors/',views.managecontractors,name='managecontractors'),



]