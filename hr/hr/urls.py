from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^blog/', include('blog.urls')),

    # Passport
    url(r'^$', 'passport.views.home', name='passport_home'),
    url(r'^passport/login/', 'passport.views.login', name='passport_login'),
    url(r'^passport/logout/', 'passport.views.logout', name='passport_logout'),

    # Staff
    url(r'^staff/$', 'staff.views.home', name='staff_home'),
    url(r'^staff/punch/$', 'staff.views.punch', name='staff_punch'),
    url(r'^staff/punch/touch/$', 'staff.views.punch_touch', name='staff_punch_touch'),
    url(r'^staff/permission/$', 'staff.views.permission', name='staff_permission'),


    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
