from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import logging

# Logging
logger = logging.getLogger(__name__)

# Method to get the main page
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            logger.info('User created successfully.')
            return redirect('note:note_list')
    else:
        form = UserCreationForm()
    logger.info('Rendering signup.')
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    logger.info('User logged out.')
    return redirect('login')

def homepage(request):
    logger.info('Rendering homepage.')
    return redirect('note:note_list')