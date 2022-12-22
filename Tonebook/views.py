import json
from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth

#This is to render the index page
def index(request):
    return render(request, 'index.html')

#This is rendering the register page as well as the functionality on whether to allow successfull submission of register form
def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        if User.objects.filter(username=request.POST["username"]).exists():
            return render(request, "register.html", {
                "error": "The username you have used already exists."
            })

        user = User()
        user.username = request.POST['username']
        user.set_password(request.POST['password'])
        user.save()

        return render(request, "register.html", {
            "error": "You have successfully signed up"
        })
    
    return render(request, "register.html", {})

#This will render the login page as well as authenticate the user
def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if auth.authenticate(request, username=username, password=password):
            auth.login(request, User.objects.get(username=username))
            return redirect("account")
        
        # Not successful in the log in
        return render(request, "login.html", {
            "error": "Your credentials are incorrect, or your account does not exist."
        })

    return render(request, "login.html", {
        "info": "Please, enter your credentials."
    })

#This is to logout the user from the application
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("login")

#This is to render the main.html page
def main(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, 'main.html')

#This is to render the account page which is the first thing you see when you login
def account(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, 'account.html')

#This is to render the files the user has asked to be rendered
def edit(request, file_id):
    if not request.user.is_authenticated:
        return redirect("login")

    user = User.objects.get(username=request.user.username)
    file = user.files.filter(id=file_id)

    if not file.exists():
        return render(request, 'error.html', {
            "error": "Not authorised",
            "description": "This file either does not exist or you are not the owner of the file"
        })

    file = file.get(id=file_id)

    content = json.dumps(file.full_obj())

    return render(request, 'edit.html', {
        "file": content,
        "name": file.name
    })
