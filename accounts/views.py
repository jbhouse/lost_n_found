from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView,DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import JsonResponse

from . import forms

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signup.html"
