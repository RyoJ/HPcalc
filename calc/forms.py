from django import forms
from django.forms import Textarea
from .models import Status, Index


class StatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ('hp', 'mp', 'event', 'detail')
        widgets = {
            'event': Textarea(attrs={'cols': 60, 'rows': 1}),
            'detail': Textarea(attrs={'cols': 90, 'rows': 12}),
   }

class IndexForm(forms.ModelForm):

    class Meta:
        model = Index
        fields = ('lossap', 'dmg', 'usemp', 'behavior', 'time')