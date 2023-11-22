import re

from My_site.settings import BASE_DIR#, STATICFILES_DIRS
#from django.conf.global_settings import STATICFILES_DIRS
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
import requests
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from .forms import *
from .utils import *


def index(request):
    #print('base: ', BASE_DIR)
    #print('base_dirs: ', STATICFILES_DIRS)
    return render(request, 'base.html')


def addsite(request):
    eror = ''
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            userr = form.save(commit=False)
            userr.user = request.user
            userr.save()
            url = form.cleaned_data.get('url')
            response = requests.get(url)
            response.url = reverse('vpn', args=(url,))
            return redirect('vpn', url)
        else:
            eror = 'Форма заповнена неправильно'
    form = SiteForm()
    return render(request, 'addpage.html', {'form': form, 'menu': menu, 'title': 'addpage', 'error':eror})


def vpn(request, path_url):
    response = requests.get(path_url)
    data_sentt = len(request.body)
    path_url_tmp = re.findall('(https?://[\w.-]+)', path_url)
    site = Site.objects.get(url=path_url_tmp[0]+'/', user=request.user)
    from_path = request.META.get('HTTP_REFERER', 'Unknown')
    to_path = f"{from_path}/{path_url}"
    SiteStats.objects.create(
        site=site,
        user=request.user,
        from_path=from_path,
        to_path=to_path,
        data_sent=data_sentt,
        data_received=len(response.content)
    )
    return HttpResponse(response)


def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


@login_required
def statistics(request):
    path = '/addsite/'
    if request.method == 'POST':
        form_username = UsernameForm(request.POST)
        form_email = EmailForm(request.POST)
        if form_username.is_valid():
            request.user.username = form_username.cleaned_data['username']
            request.user.save()
            messages.success(request, 'username змінено')
        if form_email.is_valid():
            request.user.email = form_email.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Почту змінено')
    else:
        form_username = UsernameForm()
        form_email = EmailForm()
    sites = Site.objects.filter(user=request.user)
    stats = SiteStats.objects.filter(user=request.user)

    return render(request, 'cabinet.html', {'stats': stats, 'sites': sites, 'path': path, 'form_username': form_username, 'form_email':form_email})
# Create your views here.
