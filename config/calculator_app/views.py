from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from . import operations

def home(request):
    context = {}
    if request.method == "POST":
        action = request.POST.get("action")
        try:
            num1 = float(request.POST.get("num1",0))
            num2 = float(request.POST.get("num2",0))
        except ValueError:
            context["message"]= "Please enter Valid numbers"
            return render(request,'calculator_app/home.html',context)
        
        if action == "addition":
            result = operations.add(num1, num2)
            context["message"] = f"Result: {num1} + {num2} = {result}"
            
        elif action == "subtraction":
            result = operations.subtract(num1, num2)
            context["message"] = f"Result: {num1} - {num2} = {result}"
        
        elif action == "multiplication":
            result = operations.multiply(num1, num2)
            context["message"] = f"Result: {num1} * {num2} = {result}"
            
        elif action == "division":
            result = operations.divide(num1, num2)
            context["message"] = f"Result: {num1} / {num2} = {result}"


    return render(request,'calculator_app/home.html',context)

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request,"calculator_app/signup.html",{"form":form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request,"calculator_app/login.html",{"form": form})

def logout_view(request):
    if request.method== "POST":
        logout(request)
        return redirect('login')
    return redirect('home')