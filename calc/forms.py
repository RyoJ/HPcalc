from django import forms


class StatusForm(forms.Form):
    hp = forms.IntegerField(
        label='hp',
        required=True,
        #widget=forms.TextInput() #数値の場合は必要ない？
    )

    mp = forms.IntegerField(
        label='mp',
        required=True,
        #widget=forms.TextInput() #数値の場合は必要ない？
    )

    event = forms.CharField(
        label='event',
        max_length=100,
        required=True,
        widget=forms.TextInput()
    )