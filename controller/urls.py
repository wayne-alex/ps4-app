from django.urls import path

from controller import views

urlpatterns = [
    path('', views.login, name='login'),
    path('sign_up/', views.register, name='signUp'),
    path('profile/', views.profile, name='profile'),
    path('add_profile/', views.add_profile, name='addProfile'),
    path('my_device/', views.add_device, name='addDevice'),
    path('dashboard/<int:profile_id>/', views.dashboard, name='dashboard'),
    path('test_vibration/', views.test_vibration, name='testVibration'),
    path('configure_LED/', views.configure_LED, name='configureLED'),
    path('battery_status/', views.battery_status, name='batteryStatus'),
    path('macro_hotkeys/', views.macro_hotkeys, name='macroHotkeys'),
    path('input_monitor/', views.input_monitor, name='inputMonitor'),
    path('connection_error/', views.connection_error, name='connectionError'),
    path('screenshot/', views.screenshot, name='screenshot'),
    path('add-controller/', views.add_controller, name='addController'),
]
