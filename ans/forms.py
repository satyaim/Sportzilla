from django import forms
from .models import *


class QSForm(forms.Form):
	answer=forms.CharField(max_length=50)