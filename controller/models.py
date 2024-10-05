from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#FF0000')
    total_playtime = models.IntegerField(default=0)
    total_buttons_pressed = models.IntegerField(default=0)
    right_stick_usage = models.FloatField(default=0)
    left_stick_usage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class Screenshot(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='screenshots/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Screenshot for {self.profile.name} uploaded on {self.uploaded_at}"


class Gamepad(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='gamepads')
    name = models.CharField(max_length=100)
    vendor_id = models.CharField(max_length=10)
    product_id = models.CharField(max_length=10)
    last_used = models.DateTimeField(auto_now=True)

    # RGB LED values (0-255 for each color)
    led_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    led_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    led_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])

    # LED brightness (0-100 for overall brightness)
    led_brightness = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return (f"{self.name} ({self.vendor_id}:{self.product_id}) - "
                f"LED RGB: ({self.led_red}, {self.led_green}, {self.led_blue}), "
                f"Brightness: {self.led_brightness}%")


class Game(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='games')
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=500)
    last_played = models.DateTimeField(null=True, blank=True)
    total_playtime = models.DurationField(default=0)

    def __str__(self):
        return self.name


class GamepadUsageLog(models.Model):
    gamepad = models.ForeignKey(Gamepad, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Dpad press counts for DualShock PS4 gamepad
    Dpad_up = models.IntegerField(default=0)
    Dpad_down = models.IntegerField(default=0)
    Dpad_left = models.IntegerField(default=0)
    Dpad_right = models.IntegerField(default=0)
    # Button press counts for DualShock PS4 gamepad
    cross_presses = models.IntegerField(default=0)
    circle_presses = models.IntegerField(default=0)
    square_presses = models.IntegerField(default=0)
    triangle_presses = models.IntegerField(default=0)

    l1_presses = models.IntegerField(default=0)
    r1_presses = models.IntegerField(default=0)
    l2_presses = models.IntegerField(default=0)
    r2_presses = models.IntegerField(default=0)

    l3_presses = models.IntegerField(default=0)
    r3_presses = models.IntegerField(default=0)

    share_presses = models.IntegerField(default=0)
    options_presses = models.IntegerField(default=0)
    ps_presses = models.IntegerField(default=0)
    touchpad_presses = models.IntegerField(default=0)

    # Stick usage for left and right
    left_stick_usage = models.FloatField(default=0)
    right_stick_usage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.gamepad} usage at {self.timestamp}"
