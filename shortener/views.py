from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.conf import settings

from analytics.models import ClickEvent
from .models import ShortenURL
from .forms import SubmitURLForm
from .validators import validate_url

# Create your views here.
class HomeView(View):
	def get(self, request, *args, **kwargs):
		the_form = SubmitURLForm()
		ctx = {
			"title": "MRST URL Shortener",
			"form": the_form
		}
		return render(request, 'shortener/home.html', ctx)

	def post(self, request, *args, **kwargs):
		form = SubmitURLForm(request.POST)
		ctx = {
            "title": "MRST URL Shortener",
            "form": form
        }
		template = "shortener/home.html"
		if form.is_valid():
			submitted_url = validate_url(form.cleaned_data.get("url")).lower()
			submitted_shortcode = form.cleaned_data.get("custom_shortcode")

			if submitted_shortcode == "":
				obj, created = ShortenURL.objects.get_or_create(url=submitted_url)
				ctx = {
					"object": obj,
					"created": created
				}
			else:
				count = ShortenURL.objects.filter(shortcode=submitted_shortcode).count()
				if count != 0:
					ctx = {
						"shortcode": submitted_shortcode,
						"short_url": "{root_host}/{scode}".format(
										root_host=settings.DEFAULT_REDIRECT_URL,
										scode=submitted_shortcode),
						"shortcode_exists": True,
						"title": "MRST URL Shortener",
            			"form": form
					}
					return render(request, "shortener/home.html", ctx)
				else:
					obj, created = ShortenURL.objects.get_or_create(url=submitted_url)
					obj.shortcode = submitted_shortcode
					obj.save()
					ctx = {
						"object": obj,
						"created": created,
						"updated": True
					}
			if created:
				template = 'shortener/success.html'
			else:
				template = 'shortener/already-exists.html'
		return render(request, template, ctx)

def redirect_view(request, shortcode=None):
	obj = get_object_or_404(ShortenURL, shortcode=shortcode)
	ClickEvent.objects.create_event(obj)
	return HttpResponseRedirect(obj.url)