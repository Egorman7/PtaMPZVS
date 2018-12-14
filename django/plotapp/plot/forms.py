from django import forms
from plot.models import Func

class FuncForm(forms.ModelForm):
    class Meta:
        model = Func
        fields = '__all__'
