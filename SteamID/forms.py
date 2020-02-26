from django import forms


class FormID(forms.Form):
    steam_id = forms.CharField(label='Steam ID', required=True, max_length=250)

