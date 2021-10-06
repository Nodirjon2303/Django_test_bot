from django import forms
from .models import Testing
class File(forms.ModelForm):
    class Meta:
        model=Testing
        fields='__all__'