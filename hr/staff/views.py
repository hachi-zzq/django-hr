# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import json, datetime

from .models import Punch, DayOff, Permission
from django.contrib.auth.models import User
from django.db.models import Count

import warnings

warnings.filterwarnings(
    'error', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')


@login_required
def home(request):
    return render(request, 'staff_home.html', {})


@login_required
def punch(request):
    """
    考勤记录
    """

    # 这里是现在时间 + 时区
    now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    _today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today = timezone.make_aware(_today, timezone.get_default_timezone())

    # 按钮状态
    if Punch.objects.filter(user=request.user, type='ON', touch_time__gt=today):
        btn_on_status = True
    else:
        btn_on_status = False

    if Punch.objects.filter(user=request.user, type='OFF', touch_time__gt=today):
        btn_off_status = True
    else:
        btn_off_status = False


    # 今日记录
    # TODO: 迟到排行、加班排行
    # 1. 拉取今天所有打卡记录并分组
    # 2. 取得每人第一个打卡时间和最后一个打卡时间
    # 3. 排名分组

    # 今天已打卡的员工列表
    today_bunched_staffs = Punch.objects.values('user').filter(touch_time__gt=today).annotate(
        u_count=Count('user'))

    for i in today_bunched_staffs:
        i['user'] = User.objects.select_related().get(pk=i['user'])
        # 取得首个上班时间
        first_on = Punch.objects.filter(user=i['user'],
                                        touch_time__gt=today, type='ON').first()

        if not first_on:
            i['first_on'] = None
        else:
            i['first_on'] = first_on.touch_time

        # 取得最后下班时间
        end_off = Punch.objects.filter(user=i['user'],
                                       touch_time__gt=today, type='OFF').order_by('-touch_time').first()
        if not end_off:
            i['end_off'] = None
        else:
            i['end_off'] = end_off.touch_time

    # 按上班时间排序, 生成最终数据结构
    today_bunched = list(today_bunched_staffs)
    today_bunched.sort(key=lambda d: d['first_on'] or now)

    # 我的历史
    my_all_bunches = Punch.objects.filter(user=request.user).order_by('-touch_time')

    # 请假记录
    my_all_day_off = DayOff.objects.filter(user=request.user)

    return render(request, 'staff_punch.html', {
        'btn_on_status': btn_on_status,
        'btn_off_status': btn_off_status,
        'today_bunched': today_bunched,
        'my_all_bunches': my_all_bunches,
        'my_all_day_off': my_all_day_off
    })


@login_required
def punch_touch(request):
    """
    打卡机
    """
    _type = request.GET.get('type', 'ON')
    if _type != 'ON':
        _type = 'OFF'

    # 获得当前登录用户

    # 新增一条打卡记录
    _p = Punch(user=request.user, type=_type, user_agent=request.META.get('HTTP_USER_AGENT'),
               ip=request.META.get('HTTP_X_FORWARDED_FOR'), status='UNCONFIRMED')
    _p.save()

    _result = {'status': 'Success'}
    _json_result = json.dumps(_result)
    return HttpResponse(_json_result)


@login_required
def permission(request):
    my_permission = Permission.objects.filter(user=request.user)

    return render(request, 'staff_permission.html', {
        'my_permission': my_permission,
    })

