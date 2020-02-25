from django import forms


class FormID(forms.Form):
    steam_id = forms.IntegerField(label='Steam ID', required=True, min_value=0)

