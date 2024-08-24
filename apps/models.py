from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid

class App(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name="ID", editable=False)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apk_file_path = models.FileField(upload_to='apks/')
    slug = models.SlugField(default="", null=False)
    first_screen_screenshot_path = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    second_screen_screenshot_path = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    video_recording_path = models.FileField(upload_to='videos/', blank=True, null=True)
    ui_hierarchy = models.TextField(blank=True, null=True)
    screen_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
