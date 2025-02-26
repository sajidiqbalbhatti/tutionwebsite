from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact,Feedback

# Create your views here.

def contact_view(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            Contact.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home_page')
        else:
            messages.error(request, 'All fields are required!')
    
    return render(request, 'Education/home.html')     


def feedback_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        useremail=request.POST.get('useremail')
        feedback=request.POST.get('feedback')
        
        if username and useremail and feedback:
            Feedback.objects.create(username=username, useremail=useremail, feedback=feedback)
            messages.success(request, 'Your feedback has been recorded successfully!')
            return redirect('home_page')
        else:
            messages.error(request, ' fields are required!')
        
    return render(request, 'Education/home.html')