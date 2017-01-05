from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django_hosts.resolvers import reverse

from .utils import create_shortcode
from .validators import validate_url

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class ShortenURLManager(models.Manager):
	def all(self, *args, **kwargs):
		qs_main = super(ShortenURLManager, self).all(*args, **kwargs)
		qs = qs_main.filter(active=True)
		return qs

	def refresh_shortcodes(self):
		qs = ShortenURL.objects.filter(id__gte=1)
		new_codes = 0
		for q in qs:
			q.shortcode = create_shortcode(q)
			print(q.shortcode)
			q.save()
			new_codes += 1
		return "New Codes made: {i}".format(i=new_codes)

# Create your models here.
class ShortenURL(models.Model):
	url = models.CharField(max_length=220, validators=[validate_url])
	shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	objects = ShortenURLManager()

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == "":
			self.shortcode = create_shortcode(self)

		if not "http" in self.url:
			self.url = "http://" + self.url
		super(ShortenURL, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.url

	def __str__(self):
		return self.url

	def get_short_url(self):
		url_path = reverse("scode", kwargs={"shortcode": self.shortcode}, host='www', scheme='http')
		return url_path