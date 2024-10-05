from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from controller.forms import SignUpForm
from controller.models import Profile, Gamepad


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')
        else:
            messages.success(request, 'Username or password Incorrect!')
            return redirect('login')


    else:
        return render(request, 'login.html')


@login_required
def profile(request):
    profiles = Profile.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profiles': profiles})


@login_required
def add_profile(request):
    if request.method == 'POST':
        profileName = request.POST['profileName']
        profileColor = request.POST['profileColor']

        new_profile = Profile(user=request.user, name=profileName, color=profileColor)
        new_profile.save()
        return redirect('profile')
    return render(request, 'add_profile.html')


def add_device(request):
    return render(request, 'my_devices.html')


@login_required()
def dashboard(request, profile_id):
    username = request.user.username
    currentProfile = Profile.objects.get(id=profile_id)
    profiles = Profile.objects.filter(user=request.user)

    gamepads = Gamepad.objects.filter(profile=currentProfile)
    if not gamepads:
        return redirect(add_device)
    currentGamepad = gamepads.order_by('-last_used').first()

    return render(request, 'dashboard.html',
                  {'username': username, 'currentProfile': currentProfile, 'gamepad': currentGamepad})


def test_vibration(request):
    return render(request, 'test_ramble.html')


def configure_LED(request):
    return render(request, 'LED_configuration.html')


def battery_status(request):
    return render(request, 'battery_status.html')


def macro_hotkeys(request):
    return render(request, 'macro.html')


def input_monitor(request):
    return render(request, 'input_monitor.html')


def connection_error(request):
    return render(request, 'Connection Error.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('profile')

    return render(request, 'sign_up.html')
