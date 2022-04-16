from django import forms
from .models import Video

"""
sets up the form and whats on the form.
"""
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'url', 'notes']  # need to match models