from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView,DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import JsonResponse
from django.views import generic
from django.views import View
from django.shortcuts import render,redirect
from homepage.models import FoundItem,LostItem
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm,ProfileForm
from . import forms
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    print('/'*88)
    print(subject)
    print(message)
    print('/'*88)
    print(from_email)
    print(request.POST.get('to_email', ''))
    print('/'*88)
    # if subject and message and from_email:
    #     try:
    #         send_mail(subject, message, from_email, ['admin@example.com'])
    #     except BadHeaderError:
    #         return HttpResponse('Invalid header found.')
    #     return HttpResponseRedirect('/contact/thanks/')
    # else:
    #     # In reality we'd use a form class
    #     # to get proper validation errors.
    #     return HttpResponse('Make sure all fields are entered and valid.')

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

@login_required
@transaction.atomic
def view_profile(request, **kwargs):
    if request.is_ajax():
        this_user = get_object_or_404(User, pk=kwargs['pk'])
        response_data = {}
        if this_user.email != request.POST['emailAddress']:
            this_user.email = request.POST['emailAddress']
        if this_user.username != request.POST['userName']:
            this_user.username = request.POST['userName']
        this_user.profile.phone_number = request.POST['phoneNumber']
        if request.POST['emailableOption'] == 'true':
            this_user.profile.emailable = True
        else:
            this_user.profile.emailable = False
        if request.POST['textableOption'] == 'true':
            this_user.profile.textable = True
        else:
            this_user.profile.textable = False
        this_user.save()
        this_user.profile.save()
        response_data['userName'] = request.POST['userName']
        response_data['pk'] = kwargs['pk']
        return JsonResponse(response_data)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile', pk=kwargs['pk'])
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        user_lost_items = User.objects.all().prefetch_related('lostitems').get(id = kwargs['pk'])
        user_found_items = User.objects.all().prefetch_related('founditems').get(id = kwargs['pk'])
        users = User.objects.all().select_related('profile').get(id = kwargs['pk'])
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_lost_items': user_lost_items.lostitems.all(),
        'user_found_items': user_found_items.founditems.all()
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
