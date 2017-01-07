from django import forms

from .validators import validate_url, validate_shortcode

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

	custom_shortcode = forms.CharField(
		label='',
		widget = forms.TextInput(
				attrs = {
					"placeholder": "Custom Shortcode",
					"class": "form-control custom-shortcode"
				}
		),
		required=False
	)

	def clean(self):
		super(SubmitURLForm, self).clean()
		validate_shortcode(self.cleaned_data['custom_shortcode'])