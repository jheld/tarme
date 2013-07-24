from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from compression.views import CompressView, SuccessView#, CompressionTypeView
from compression.models import Document
from django.views.generic import TemplateView, ListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tarme.views.home', name='home'),
    # url(r'^tarme/', include('tarme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
                       url('^success/*$',SuccessView.as_view(),name='success'),
#url('^compression_type/$',TemplateView.as_view(template_name='compression_type.html'),name='compression_type'),
url('^document_list/*$',ListView.as_view(template_name='compression/document_list.html',model=Document),name='document_list'),
url('^\w*$',CompressView.as_view(),name='compress'),
)
