import logging

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import operations
from .operations import DivisionByZeroError
from .models import CalculationHistory

logger = logging.getLogger(__name__)

OPERATION_MAP = {
    "addition": (operations.add, "+"),
    "subtraction": (operations.subtract, "-"),
    "multiplication": (operations.multiply, "*"),
    "division": (operations.divide, "/"),
}


@login_required(login_url="login")
def home(request):
    """Calculator home view — requires authentication."""
    context = {
        "history": CalculationHistory.objects.filter(user=request.user)[:10]
    }

    if request.method == "POST":
        action = request.POST.get("action")
        try:
            num1 = float(request.POST.get("num1", 0))
            num2 = float(request.POST.get("num2", 0))
        except (ValueError, TypeError):
            messages.error(request, "Please enter valid numbers.")
            logger.warning(
                "Invalid input from user %s", request.user.username
            )
            return render(request, "calculator_app/home.html", context)

        if action not in OPERATION_MAP:
            messages.error(request, "Invalid operation.")
            return render(request, "calculator_app/home.html", context)

        func, symbol = OPERATION_MAP[action]
        try:
            result = func(num1, num2)
        except DivisionByZeroError:
            messages.error(request, "Error: Cannot divide by zero.")
            return render(request, "calculator_app/home.html", context)

        # Save to history
        CalculationHistory.objects.create(
            user=request.user,
            num1=num1,
            num2=num2,
            operation=action,
            result=result,
        )
        context["message"] = f"{num1} {symbol} {num2} = {result}"
        logger.info(
            "User %s: %s %s %s = %s",
            request.user.username, num1, symbol, num2, result,
        )

    return render(request, "calculator_app/home.html", context)


def register_view(request):
    """User registration view."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info("New user registered: %s", user.username)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "calculator_app/signup.html", {"form": form})


def login_view(request):
    """User login view."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info("User logged in: %s", user.username)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "calculator_app/login.html", {"form": form})


def logout_view(request):
    """User logout view."""
    if request.method == "POST":
        logger.info("User logged out: %s", request.user.username)
        logout(request)
        return redirect("login")
    return redirect("home")


def health_check(request):
    """Health-check endpoint for Kubernetes/Docker probes."""
    return JsonResponse({"status": "healthy"})
