from django.shortcuts import render
from django.shortcuts import redirect
from . import forms
from private_messages.forms import MessageForm
from django.views import generic
from . import models
from private_messages.models import PrivateMessage
from django.contrib.auth import get_user_model
User = get_user_model()
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages

def CreatePrivateMessage(request):
    if request.method == "POST":
        response_data = {}
        if request.user.is_authenticated():
            sender = request.user
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        recipient_id = request.POST.get('recipient')
        recipient = get_object_or_404(User, pk=recipient_id)
        new_pm = PrivateMessage.objects.create_private_message(sender,recipient)
        new_pm.subject = subject
        new_pm.message = message
        new_pm.save()
        response_data['recipient_id'] = recipient_id
        response_data['sender_id'] = sender.pk
        response_data['message_pk'] = new_pm.pk
        response_data['message'] = new_pm.message
        response_data['subject'] = new_pm.subject
        response_data['username'] = new_pm.sender.username
        response_data['recipient'] = new_pm.recipient.username
        return JsonResponse(response_data)

class PrivateMessageList(generic.TemplateView,SelectRelatedMixin,LoginRequiredMixin):
    model = models.PrivateMessage
    template_name = 'private_messages/privatemessage_list.html'

    def get(self, request, *args, **kwargs):
        message_form = MessageForm(self.request.GET or None)
        message_recipient = User.objects.prefetch_related('recipient').get(username__iexact=self.request.user.username)
        message_sender = User.objects.prefetch_related('sender').get(username__iexact=self.request.user.username)
        context = self.get_context_data(**kwargs)
        context['message_form'] = message_form
        context['users_inbox'] = message_recipient.recipient.all().order_by('-created_at')
        context['users_outbox'] = message_sender.sender.all().order_by('-created_at')
        return self.render_to_response(context)

class PrivateMessageDetail(SelectRelatedMixin,generic.DetailView):
    model = PrivateMessage
    # private_message = get_object_or_404(PrivateMessage, pk=kwargs['pk'])
    # private_message.viewed = True
    select_related = ('sender','recipient')

    def get_object(self):
        object = super(PrivateMessageDetail, self).get_object()
        object.viewed = True
        object.save()
        return object

    def query_set(self):
        queryset = super().get_queryset()
        return queryset.filter(recipient = self.request.user)

def DeletePrivateMessage(request, **kwargs):
    private_message = get_object_or_404(PrivateMessage, pk=kwargs['pk'])
    private_message.delete()
    if request.is_ajax():
        response_data = {}
        response_data['pk'] = kwargs['pk']
        return JsonResponse(response_data)
    return redirect('private_messages:list')

def DeletePrivateMessageHome(request, **kwargs):
    private_message = get_object_or_404(PrivateMessage, pk=kwargs['pk'])
    private_message.delete()
    return redirect('home')
