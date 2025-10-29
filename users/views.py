from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser

# ----------------------
# User Registration View
# ----------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")

        # Validation
        if not all([username, email, password1, password2, role]):
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

        # Create User
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role,
        )

        # Role-based permissions
        if role == "author":
            user.can_upload_books = False  # Needs staff approval
            user.is_active = True          # Keep active (but cannot upload yet)
            user.save()
            messages.info(request, "Author account created. Wait for staff approval to upload books.")
        else:
            user.can_upload_books = True
            user.is_active = True
            user.save()
            messages.success(request, "Account created successfully! You can log in now.")

        return redirect("login")

    return render(request, "users/register.html")

# ----------------------
# Login View
# ----------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("home")
            else:
                messages.warning(request, "Your account is not active yet.")
        else:
            messages.error(request, "Invalid username or password!")

        return redirect("login")

    return render(request, "users/login.html")

# ----------------------
# Logout View
# ----------------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")
