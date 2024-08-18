from django.contrib.auth.models import User
from django.db import models

class App(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apk_file_path = models.FileField(upload_to='media/apks/' )
    slug = models.SlugField(default="", null=False)
    first_screen_screenshot_path = models.ImageField(upload_to='media/screenshots/', blank=True, null=True)
    second_screen_screenshot_path = models.ImageField(upload_to='media/screenshots/', blank=True, null=True)
    video_recording_path = models.FileField(upload_to='media/videos/', blank=True, null=True)
    ui_hierarchy = models.TextField(blank=True, null=True)
    screen_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
