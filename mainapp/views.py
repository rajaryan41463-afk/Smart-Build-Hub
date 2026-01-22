from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import requests

# Create your views here.
def index(request):
    return render(request,'index.html')

def project(request):
    return render(request,'project.html')

def  about(request):
    return render(request,'about.html')
def  contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        enq=Enquiry(name=name,contactno=contactno,email=email,subject=subject,message=message)
        enq.save()
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": f"{contactno}",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }
        response = requests.get(url, params=params)
        print("Response:", response.text)
        messages.success(request,'Your Enquiry has been sucessfully submit')
        return redirect('contact')
    return render(request,'contact.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            ad= LoginInfo.objects.get(username=username,password=password,usertype="admin")
            if ad is not None:
                request.session['adminid'] = username
                messages.success(request,"welcome Admin")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"invalid username or password")
            return redirect('adminlogin')
    return render(request,'adminlogin.html')
def  service(request):
    return render(request,'service.html')


def  register(request):
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        usertype = request.POST.get('usertype')
        password = request.POST.get('password')
        u = LoginInfo.objects.filter(username = email)
        if u:
            messages.error(request,"Email already exists")
            return redirect('register')
        log = LoginInfo(usertype=usertype,username=email,password=password)
        user = userinfo(name=name,email=email,contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request,"You are registered")
        return redirect('register')
    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            log = LoginInfo.objects.get(username=username,password=password,)
            if log is not None:
                if log.usertype.lower() == "homeowner":
                    request.session['homeownerid'] = username
                    messages.success(request,"Welcome Homeowner")
                    return redirect('homeownerdash')
                elif log.usertype.lower() == "contractor":
                    request.session['contractorid'] = username
                    messages.success(request," Welcome contractor ") 
                    return redirect('contractordash')
                else:
                    messages.error(request,"Something went wrong") 
                    return redirect('login')  
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid User Name and Password")
            return redirect('login')              
    return render(request,'login.html')




 
