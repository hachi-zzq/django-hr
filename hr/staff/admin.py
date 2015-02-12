from django.contrib import admin
from .models import Punch, DayOff, Permission


class PunchAdmin(admin.ModelAdmin):
    list_display = ('touch_time', 'user', 'type', 'ip')


class DayOffAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'start_at', 'end_at', 'total_time','status')


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'app_name', 'username', 'password', 'status')


admin.site.register(Punch, PunchAdmin)
admin.site.register(DayOff, DayOffAdmin)
admin.site.register(Permission, PermissionAdmin)