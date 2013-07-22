from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from compression.views import CompressView
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tarme.views.home', name='home'),
    # url(r'^tarme/', include('tarme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
                       url('^success/*$',TemplateView.as_view(template_name='success.html'),name='success'),
url('^\w*$',CompressView.as_view(),name='compress'),
)
