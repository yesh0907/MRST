from django import forms

from .validators import validate_url

class SubmitURLForm(forms.Form):
	url = forms.CharField(
		label='', 
		validators=[validate_url],
		widget = forms.TextInput(
				attrs={
					"placeholder": "URL To Shorten",
					"class": "form-control"
				}
			)
		)