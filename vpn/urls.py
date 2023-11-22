from django.conf import settings
from django.urls import path, re_path
from .views import *
from django.views.static import serve

urlpatterns = [
    path('', index, name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('cabinet/', statistics, name='cabinet'),
    path('addsite/', addsite, name='addsite'),
    path('addsite/<path:path_url>', vpn, name='vpn'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]