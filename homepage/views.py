from django.shortcuts import render
from django.views import generic

# Create your views here.
class Home(generic.TemplateView):
    template_name = "homepage/home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
