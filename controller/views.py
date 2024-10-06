import base64

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from controller.forms import SignUpForm
from controller.models import Profile, Gamepad, Screenshot


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

    # if not gamepads:
    #     return redirect(add_device)
    # currentGamepad = gamepads.order_by('-last_used').first()

    screenshots = Screenshot.objects.all()

    return render(request, 'dashboard.html',
                  {'username': username, 'currentProfile': currentProfile, 'screenshots': screenshots})


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


@csrf_exempt
def screenshot(request):
    if request.method == 'POST':
        try:
            img_base64 = request.POST.get('image')
            if not img_base64:
                return JsonResponse({'error': 'No image data received'}, status=400)
            img_data = base64.b64decode(img_base64)
            screenshot_ = Screenshot()
            screenshot_.image.save('screenshot.png', ContentFile(img_data), save=True)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required()
@csrf_exempt
def add_controller(request):
    if request == 'POST':
        profile_ = Profile.objects.get(user=request.user)
        controller_VendorID = request.POST['vendor_id']
        controller_productID = request.POST['product_id']

        add_gamepad = Gamepad(profile=profile_, name='DualSense4', vendor_id=controller_VendorID,
                              product_id=controller_productID)
        add_gamepad.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('Not ok')


@login_required
def delete_screenshot(request, screenshot_id, profile_id):
    _screenshot = get_object_or_404(Screenshot, id=screenshot_id)
    if request.method == 'POST':
        _screenshot.delete()
        messages.success(request, "Screenshot deleted successfully!")
        return redirect('dashboard', profile_id=profile_id)
    return redirect('dashboard', profile_id=profile_id)
