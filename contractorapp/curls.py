from django.urls import path
from . import views

urlpatterns = [

    path('contractordash/',views.contractordash,name='contractordash'),
    path('contractorlogout/',views.contractorlogout, name='contractorlogout'),
    path('contractorpass/',views.contractorpass,name='contractorpass'),
    path('contractorprofile/',views.contractorprofile,name='contractorprofile'), 
    path('contractoredit/',views.contractoredit,name='contractoredit'),
    path('contractorviewproject/',views.contractorviewproject,name='contractorviewproject'), 
    path('applyproject/<id>',views.applyproject,name='applyproject'),
    path('contractorapplications/',views.contractorapplications,name='contractorapplications'),
    path('assignedproject/',views.assignedproject,name='assignedproject'), 
    path('addprogress/<id>',views.addprogress,name='addprogress'),

]