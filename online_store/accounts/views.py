from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('login')  # Redirect to login page after successful sign-up
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to appropriate dashboard based on role or superuser status
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('role_based_home')  # This handles vendor and customer redirection
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def role_based_home(request):
    if request.user.is_authenticated:
        # Check the user's role and redirect accordingly
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.role == 'vendor':
            return redirect('vendor_dashboard')
        elif request.user.role == 'customer':
            return redirect('browse_products')
    return redirect('login')  # Redirect to login if user is not authenticated
