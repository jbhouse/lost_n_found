from django.shortcuts import render,redirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
class Home(generic.TemplateView):
    template_name = "homepage/home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')

@login_required
def CreateLostItem(request, **kwargs):
    if request.method == "POST":
        response_data = {}
        if request.user.is_authenticated():
            user = request.user
            new_lost_item = LostItem.objects.create_lost_item(user)
            print('-'*50)
            print(request.POST)
            print('-'*50)
