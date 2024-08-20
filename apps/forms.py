from django import forms
from .models import App

class CreateApp(forms.ModelForm):
    class Meta:
        model = App
        fields = [
            'name', 
            'apk_file_path'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'App Name'})
        }