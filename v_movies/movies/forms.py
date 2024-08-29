from .models import SerialComments, MovieComments
from django import forms


class SerialCommentsForm(forms.ModelForm):
    class Meta:
        model = SerialComments
        fields = ("name", "body")

class MovieCommentsForm(forms.ModelForm):
    class Meta:
        model = MovieComments
        fields = ("name", "body")
