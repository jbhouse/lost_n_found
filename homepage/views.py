from django.shortcuts import render,redirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from homepage.models import LostItem,FoundItem
from django.http import JsonResponse

# Create your views here.
class Home(generic.TemplateView):
    template_name = "homepage/home.html"

    def get(self, request, *args, **kwargs):
        lost_items = list(LostItem.objects.all())
        lost_items_array = []
        for idx,item in enumerate(lost_items):
            hsh = {"description":item.description,"latitude":item.latitude,"longitude":item.longitude,"user_id":item.user.pk}
            lost_items_array.append(hsh)
        found_items = list(FoundItem.objects.all())
        found_items_array = []
        for idx,item in enumerate(found_items):
            hsh = {"description":item.description,"latitude":item.latitude,"longitude":item.longitude,"user_id":item.user.pk}
            found_items_array.append(hsh)
        return self.render_to_response({'found_items_array': found_items_array, 'lost_items_array': lost_items_array})

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
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            description = request.POST.get('description')
            new_lost_item = LostItem.objects.create_lost_item(user, latitude, longitude, description)
            new_lost_item.save
            response_data['user_id'] = user.pk
            response_data['latitude'] = latitude
            response_data['longitude'] = longitude
            response_data['description'] = description
        return JsonResponse(response_data)


@login_required
def CreateFoundItem(request, **kwargs):
    if request.method == "POST":
        response_data = {}
        if request.user.is_authenticated():
            user = request.user
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            description = request.POST.get('description')
            new_found_item = FoundItem.objects.create_found_item(user, latitude, longitude, description)
            new_found_item.description = description
            new_found_item.save
            response_data['user_id'] = user.pk
            response_data['latitude'] = latitude
            response_data['longitude'] = longitude
            response_data['description'] = description
        return JsonResponse(response_data)
