# -*- coding: UTF-8 -*-

__author__ = 'luyu'

from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail


class CheckOnReport(CronJobBase):
    RUN_AT_TIMES = ['13:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'staff.check_on_report'    # a unique code

    # 读邮件模版
    # 昨日下班考勤列表
    # 今日上班考勤列表

    def do(self):
        send_mail('[HR]考勤简报 2014.1.21',
                  '''
                  Dear All,

                  此为 HR 系统自动生成的考勤报告，为您报告昨日与今日的考勤简报。

                  >>> 昨日 2014年1月20日 星期一 下班考勤明细
                  正常打卡的员工：李冠军(09:00)、朱鋆(09:00)、张路宇(09:00)
                  非正常打卡的员工有：张敏(未打卡)、季土豪(10:00)

                  >>> 今日 2014年1月21日 星期一 上班考勤明细
                  正常打卡的员工：李冠军(09:00)、朱鋆(09:00)、张路宇(09:00)
                  非正常打卡的员工有：张敏(未打卡)、季土豪(10:00)


                  祝工作顺利！

                  AutoTiming HR System
                  http://hr.autotiming.com/

                  ''',
                  'hr-suzhou@autotiming.com',
                  ['luyu.zhang@autotiming.com'],
                  fail_silently=False)