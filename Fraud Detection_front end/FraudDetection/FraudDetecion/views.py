from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_control
from ProfilePic.models import Profile
import re
from django.http import JsonResponse



@login_required(login_url='login')
def dashboard(request):
    user = request.user  # Get the currently logged-in user
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, "dashboard.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    if request.method == 'POST':
        userid = request.POST.get('userId')
        password = request.POST.get('password')
        user = authenticate(request, username=userid, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid User ID or Password')
    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        userid = request.POST.get('userId')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Check if all required fields are provided
        if not all([first_name, last_name, userid, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, "registration.html")

        # Validate password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, "registration.html")

        # Validate email format (basic check)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Invalid email format.')
            return render(request, "registration.html")

        try:
            # Check if user already exists
            if User.objects.filter(username=userid).exists():
                messages.error(request, 'User ID already exists.')
                return render(request, "registration.html")

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, "registration.html")

            # Create user
            user = User.objects.create_user(
                username=userid,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            # Create Profile for the new user
            Profile.objects.create(user=user)

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')

    return render(request, "registration.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully!')
            return redirect('login')  # Redirect to login after password change
    return redirect('dashboard')  # Handle GET requests if needed
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profilePicture')

        # Update user information
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        # Ensure profile exists
        profile, created = Profile.objects.get_or_create(user=user)

        if profile_picture:
            user.profile.profile_picture = profile_picture  # Assuming a One-to-One relationship with a Profile model
            user.profile.save()

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('dashboard')  # Redirect to the dashboard or any desired page

    return redirect('edit_profile')  # Redirect back if method is not POST