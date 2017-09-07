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
from homepage.models import FoundItem,LostItem
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm,ProfileForm

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

# @login_required
# @transaction.atomic
# class ViewProfile(generic.DetailView):
#     model = User
#     template_name = 'accounts/profile.html'
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         def get_context_data(self, **kwargs):
#             context = super(ViewProfile, self).get_context_data(**kwargs)
#             self.user_lost_items = User.objects.all().prefetch_related('lostitems').get(id = self.kwargs['pk'])
#             self.user_found_items = User.objects.all().prefetch_related('founditems').get(id = self.kwargs['pk'])
#             context['user_lost_items'] = list(self.user_lost_items.lostitems.all())
#             context['user_found_items'] = list(self.user_found_items.founditems.all())
#             return context
#         context = get_context_data(self)
#         return render(request, 'accounts/profile.html', context)

@login_required
@transaction.atomic
def view_profile(request, **kwargs):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def DeleteFoundItem(request, **kwargs):
    founditem = get_object_or_404(FoundItem, pk=kwargs['pk'])
    founditem.delete()
    user_id = founditem.user.pk
    if request.is_ajax():
        response_data = {}
        response_data['pk'] = kwargs['pk']
        return JsonResponse(response_data)
    return redirect('accounts:profile', pk=user_id)

def DeleteLostItem(request, **kwargs):
    lostitem = get_object_or_404(LostItem, pk=kwargs['pk'])
    lostitem.delete()
    user_id = lostitem.user.pk
    if request.is_ajax():
        response_data = {}
        response_data['pk'] = kwargs['pk']
        return JsonResponse(response_data)
    return redirect('accounts:profile', pk=user_id)
