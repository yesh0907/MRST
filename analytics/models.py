from __future__ import unicode_literals

from django.db import models

from shortener.models import ShortenURL

class ClickEventManager(models.Manager):
	def create_event(self, short_url):
		if isinstance(short_url, ShortenURL):
			obj, created = self.get_or_create(shorten_url=short_url)
			obj.count += 1
			obj.save()
			return obj.count
		return None


# Create your models here.
class ClickEvent(models.Model):
	shorten_url = models.OneToOneField(ShortenURL)
	count = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	objects = ClickEventManager()

	def __str__(self):
		return "{url}: {i} Clicks".format(url=self.shorten_url.url, i=self.count)