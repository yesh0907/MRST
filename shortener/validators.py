from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_url(url):
	url_validator = URLValidator()
	reg_url = url

	if "http" in reg_url:
		new_url = reg_url
	else:
		new_url = "http://" + reg_url

	try:
		url_validator(new_url)
	except:
		raise ValidationError("Invalid URL")

	return new_url

def validate_shortcode(shortcode):
	if len(shortcode) != 0:
		if len(shortcode) < 4:
			raise ValidationError("Shortcode too short! Minimum is 4")
		elif len(shortcode) > 15:
			raise ValidationError("Shortcode too long! Maximum is 15")

	return shortcode