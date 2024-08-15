from django import forms
from .models import App

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = [
            'name', 
            'apk_file_path', 
            'first_screen_screenshot_path',
            'second_screen_screenshot_path',
            'video_recording_path',
            'ui_hierarchy',
            'screen_changed'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'App Name'}),
            'ui_hierarchy': forms.Textarea(attrs={'placeholder': 'UI Hierarchy'}),
        }