from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser


# ------------------ REGISTER VIEW ------------------

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")

        if not username or not email or not password1 or not password2:
            messages.error(request, "Please fill all fields.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role
        )

        if role == "author":
            user.can_upload_books = False
            user.save()
            messages.info(request, "Author account created. Wait for admin approval.")
        else:
            user.can_upload_books = True
            user.save()
            messages.success(request, "Account created successfully! You can login now.")

        return redirect("login")

    return render(request, "users/register.html")

# ------------------ LOGIN VIEW ------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("home")
            else:
                messages.warning(request, "Your account is not active yet.")
                return redirect("login")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")

    return render(request, "users/login.html")


# ------------------ LOGOUT VIEW ------------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")
