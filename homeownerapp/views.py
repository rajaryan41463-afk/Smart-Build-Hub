from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from.forms import ProjectForm
from homeownerapp.models import *
from contractorapp.models import*
from django.utils import timezone
# Create your views here.

    

def  homeownerdash(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid
    }
    return render(request,'homeownerdash.html',context)   

def homeownerlogout(request):
    if 'homeownerid' in request.session:
        del request.session['homeownerid']
        messages.success(request,"you are logged out")
        return redirect('login')
    else:
        return redirect('login')
    


def  homeownerpass(request):
    if not 'homeownerid' in request.session:
        messages.error(request, "you are not logged in")
        return redirect('homeownerlogin')
    homeownerid = request.session.get('homeownerid')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd =request.POST.get('newpwd')  
        confirmpwd =request.POST.get('confirmpwd')
        try:
            homeowner = LoginInfo.objects.get(username=homeownerid)
            if homeowner.password != oldpwd:
                messages.error(request, "old password is incorrect")
                return redirect('homeownerpass')
            elif newpwd != confirmpwd:
                messages.error(request,"New password and old password not match")
                return redirect('homeownerpass')
            elif homeowner.password == newpwd:
                messages.error(request,"New password is same as old password")
                return redirect('homeownerpass')
            else:
                homeowner.password = newpwd
                homeowner.save()
                messages.success(request,"password changed successfully")
                return redirect('homeownerdash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Somthing went wrong")
            return redirect('homeownerlogin')            
    return render(request,'homeownerpass.html',{'homeownerid':homeownerid})


def  homeownerprofile(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner,
    }
    return render(request,'homeownerprofile.html',context)


def  homeowneredit(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner,
    }
    if request.method == "POST":
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')
        homeowner.name = name
        homeowner.contactno = contactno
        homeowner.address = address
        homeowner.bio = bio
        if profile:
            homeowner.picture = profile
        homeowner.save()
        messages.success(request,"Your Profilr has been updated")
        return redirect('homeownerprofile')
    return render(request,'homeowneredit.html',context)

    
def  addproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    form = ProjectForm()
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'form':form
    }
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.homeowner = homeowner
            project.save()
            messages.success(request,"Your Project has been added")
            return redirect('addproject')
        else:
            messages.error(request,"invalid form")
            return redirect('addproject')
    return render(request,'addproject.html',context)   


def  homeownerviewproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner)
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects' : projects
    }
    return render(request,'homeownerviewproject.html',context)   

def  homeownerviewapplications(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    applications = ContractorApplication.objects.filter(project=project)
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'applications':applications,
    }
    return render(request,'homeownerviewapplications.html',context)   

def  rejectapp(request,id):


    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    app = ContractorApplication.objects.get(id=id)
    app.status= 'rejected'
    app.save()
    messages.success(request,"Application has been rejected")
    return redirect('homeownerviewapplications',id=app.project.id)


def  approveapp(request,id):


    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()    
    app = ContractorApplication.objects.get(id=id)
    project = Project.objects.get(id=app.project.id)
    apps = ContractorApplication.objects.filter(project=app.project).update(status="rejected")
    app.status= 'approved'
    app.save()
    project.contractor = app.contractor
    project.start_date = timezone.now()
    project.status = 'under_construction'
    project.save()
    messages.success(request,"Application has been Approved")
    return redirect('homeownerviewapplications',id=app.project.id)


def  runningprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner,status='under_construction')
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects
        
    }
    return render(request,'runningprojects.html',context) 


def  viewupdates(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    updates = ProgressUpdate.objects.filter(project=project)
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'updates':updates
    }
    return render(request,'viewupdates.html',context) 


def  homeownercompletedprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    projects =Project.objects.filter(homeowner=homeowner,status='completed')
    context ={
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects': projects,

    }
    return render(request,'homeownercompletedprojects.html',context)