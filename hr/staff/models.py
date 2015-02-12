# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Punch(models.Model):
    """
    打卡表
    """
    user = models.ForeignKey(User, related_name='+')

    touch_time = models.DateTimeField(auto_now=True)

    STATUS = (
        ('CONFIRMED', '已确认'),
        ('UNCONFIRMED', '未确认'),
        ('INVALID', '被拒绝'),
    )

    PUNCH_TYPE = (
        ('ON', '上班'),
        ('OFF', '下班'),
    )
    type = models.CharField(max_length=16, choices=PUNCH_TYPE)
    user_agent = models.TextField(max_length=512)
    ip = models.IPAddressField()
    status = models.CharField(max_length=32, choices=STATUS)
    reviewers = models.OneToOneField(User, null=True, blank=True, related_name='+')


class DayOff(models.Model):
    """
    请假表
    """

    STATUS = (
        ('CONFIRMED', '已确认'),
        ('UNCONFIRMED', '未确认'),
        ('INVALID', '被拒绝'),
    )

    user = models.ForeignKey(User, related_name='+')
    type = models.CharField(max_length=32)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    total_time = models.IntegerField() # 单位为小时
    cause = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS)
    reviewers = models.ForeignKey(User, null=True, blank=True, related_name='+')


class Permission(models.Model):
    """
    账号权限
    """

    STATUS = (
        ('ENABLE', '可用'),
        ('DISABLED', '禁用'),
    )

    user = models.ForeignKey(User, related_name='+')
    app_name = models.CharField(max_length=100)
    username = models.CharField(max_length=64)
    password = models.CharField(null=True, blank=True, max_length=64)
    note = models.CharField(null=True, blank=True, max_length=100)
    status = models.CharField(max_length=32, choices=STATUS)
    reviewers = models.ForeignKey(User, null=True, blank=True, related_name='+')
