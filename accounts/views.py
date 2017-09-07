from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView,DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import JsonResponse
from django.views import generic
from django.views import View
from django.shortcuts import render

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

class ViewProfile(generic.DetailView):
    model = User
    template_name = 'accounts/profile.html'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        def get_context_data(self, **kwargs):
            context = super(ViewProfile, self).get_context_data(**kwargs)
            self.user_lost_items = User.objects.all().prefetch_related('lostitems').get(id = self.kwargs['pk'])
            self.user_found_items = User.objects.all().prefetch_related('founditems').get(id = self.kwargs['pk'])
            context['user_lost_items'] = list(self.user_lost_items.lostitems.all())
            context['user_found_items'] = list(self.user_found_items.founditems.all())
            return context
        context = get_context_data(self)
        return render(request, 'accounts/profile.html', context)

def DeleteFoundItem(request, **kwargs):
    print('/'*50)
    print('/'*50)
    print('/'*50)

def DeleteLostItem(request, **kwargs):
    print('/'*50)
    print('/'*50)
    print('/'*50)
