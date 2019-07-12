from django import forms
from .models import Status, Index


class StatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ('hp', 'mp', 'event')
        
class IndexForm(forms.ModelForm):

    class Meta:
        model = Index
        fields = ('lossap', 'dmg', 'usemp', 'behavior', 'time')