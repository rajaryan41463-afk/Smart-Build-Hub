from django.urls import path
from . import views

urlpatterns = [

   path('homeownerdash/',views.homeownerdash, name='homeownerdash'),
   path('homeownerlogout/',views.homeownerlogout, name='homeownerlogout'),
   path('homeownerpass/',views.homeownerpass,name='homeownerpass'),
   path('homeownerprofile/',views.homeownerprofile,name='homeownerprofile'), 
   path('homeowneredit/',views.homeowneredit,name='homeowneredit'), 
   path('addproject/',views.addproject,name='addproject'),
   path('homeownerviewproject/',views.homeownerviewproject,name='homeownerviewproject'),  
   path('homeownerviewapplications/<id>',views.homeownerviewapplications,name='homeownerviewapplications'), 
   path('rejectapp/<id>',views.rejectapp,name='rejectapp'),
   path('approveapp/<id>',views.approveapp,name='approveapp'),
   path('runningprojects/',views.runningprojects,name='runningprojects'),  
   path('viewupdates/<id>',views.viewupdates,name='viewupdates'),
   path('homeownercompletedprojects/',views.homeownercompletedprojects,name='homeownercompletedprojects'),  


]  