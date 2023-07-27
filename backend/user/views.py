from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginFrom
from send_email.models import Contact
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You successfully registered!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Registration error.')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginFrom(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You successfully logged in!')
            return redirect('user_profile')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserLoginFrom()
    return render(request, 'user/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def user_profile(request):
    if request.user.is_authenticated:
        contact_user = Contact.objects.filter(user=request.user).exists()
        context = {
            'title': 'User Profile',
            'contact_user': contact_user,
        }
        return render(request, 'user/user_profile.html', context=context)
    else:
        return redirect('login')


def user_response(request):
    response = f'Hello {request.user}'
    return render(request, 'user/response.html', {'response': response})
