from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

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
			submitted_url = validate_url(form.cleaned_data.get("url"))
			obj, created = ShortenURL.objects.get_or_create(url=submitted_url)
			ctx = {
				"object": obj,
				"created": created
			}
			if created:
				template = 'shortener/success.html'
			else:
				template = 'shortener/already-exists.html'
		return render(request, template, ctx)

def redirect_view(request, shortcode=None):
	obj = get_object_or_404(ShortenURL, shortcode=shortcode)
	# save item
	ClickEvent.objects.create_event(obj)
	return HttpResponseRedirect(obj.url)