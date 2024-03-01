from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "index.html"


class Healthcheck(View):
    def get(self, request):
        return HttpResponse("OK")
