# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from django import forms

import requests


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=48)
    remember_me = forms.BooleanField(required=False)


def _login_redmine(username, password):
    r = requests.get('http://pd.autotiming.com/users/current.json', auth=(username, password))
    if r.status_code == 200:
        user = r.json()
    else:
        user = None

    if user:
        return user.get('user')
    else:
        return False


def home(request):
    return redirect('/staff/')


def login(request):
    login_status = None
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            # 优先使用本系统验证登录
            _next = request.GET.get('next', '/staff/') # 这里的 GET 参数目前取不到
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            _remember_me = form.cleaned_data['remember_me']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect(_next)
                else:
                    login_status = 'DISABLED'
            else:
                # 如验证失败则调取 PD 用户登录
                _pd_user = _login_redmine(username, password)
                if _pd_user:
                    # PD 登录成功
                    try:
                        user = User.objects.get(username=_pd_user.get('login'))
                        user.set_password(password)
                        user.save()
                        user = auth.authenticate(username=username, password=password)
                    except User.DoesNotExist:
                        # 不存在的用户则创建
                        _new_user = User.objects.create_user(_pd_user.get('login'), _pd_user.get('mail'), password)
                        _new_user.last_name = _pd_user.get('lastname')
                        _new_user.first_name = _pd_user.get('firstname')
                        _new_user.save()
                        user = auth.authenticate(username=username, password=password)

                    # 保存登录身份
                    auth.login(request, user)
                    return redirect(_next)
                else:
                    # PD 登录失败
                    login_status = 'FAILED'
    else:
        form = LoginForm() # An unbound form

    return render(request, 'login.html', {
        'form': form,
        'login_status': login_status,
    })


def logout(request):
    auth.logout(request)
    return redirect('/')