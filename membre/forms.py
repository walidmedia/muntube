from .models import Video
from django import forms

"""class Video_form(forms.ModelForm):
    user  = forms.CharField()
    title  = forms.CharField(label="Enter last name", max_length = 10)
    detail  = forms.CharField(label="Enter last name", max_length = 10)
    vid = forms.FileField()
    img = forms.FileField()
    class Meta:
        model=Video
        fields=("user","title","detail","vid","img")"""