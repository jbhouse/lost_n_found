from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'


urlpatterns = [
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='profile'),
    url(r'^email/$', views.send_email, name='email'),
    url(r'^delete/founditem/(?P<pk>\d+)/$', views.DeleteFoundItem, name='found_delete'),
    url(r'^delete/lostitem/(?P<pk>\d+)/$', views.DeleteLostItem, name='lost_delete'),
]
