from django.conf.urls import patterns, include, url
from insurance.views import *
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/$',login),
    (r'^time/$',current_datatime),
    (r'^signup/$',signup),
    (r'^advancedSearch/$',advancedSearch),
    (r'^advancedSearch2/$',advancedSearch2),
    (r'^advanceduserSearch/$',advanceduserSearch),
    (r'^advanceduserSearch2/$',advanceduserSearch2),
    (r'^commonuserRecommend/$',commonuserRecommend),
    (r'^retrievePassword/$',retrievePassword),
    (r'^sendPassword/$',sendPassword),
    (r'^resetPassword/$',resetPassword),
    (r'^resetPassword2/$',resetPassword2),
    (r'^contactUs/$',contactUs),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/insurance/media'})
    #(r'^media/(?P.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH})
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_PATH})
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT },name="media")
    # Examples:
    # url(r'^$', 'insurance.views.home', name='home'),
    # url(r'^insurance/', include('insurance.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
