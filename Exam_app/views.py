from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "index.html")

def success(request):
    user_object = User.objects.get(id=request.session['user_id'])
    context = {
        'first_name': user_object.first_name
    }
    return render(request, "success.html", context)

def register(request):
    errors = User.objects.reg_val(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hashed_pw
            )
        request.session['user_id'] = new_user.id
        return redirect('/success')

def login(request):
    user = User.objects.filter(email=request.POST['email'])

    if user:    
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/success')
    
    messages.error(request, "Invalid email/password", extra_tags="login")
    return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')