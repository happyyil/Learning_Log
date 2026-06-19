from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserForm, ProfileForm

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.   
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('learning_logs:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def logged_out(request):
    """Display a message indicating that the user has logged out."""
    logout(request)
    print("User logged out")
    return render(request, 'learning_logs/logged_out.html')

def password_reset_done(request):
    return redirect('users:password_reset/done')


@login_required
def profile(request):
    """用户个人档案"""
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method != 'POST':
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    else:
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile')

    context = {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/profile.html', context)