from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from compression.views import CompressView, CompressDeleteView, SuccessView, DocumentUploadView#, getAuthUrl, callback_handler#, tweet, update
from compression.models import Document
from django.views.generic import TemplateView, ListView, DetailView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tarme.views.home', name='home'),
    # url(r'^tarme/', include('tarme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
                       url('^success/{0,1}$',SuccessView.as_view(),name='success'),
                       url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
#url('^compression_type/$',TemplateView.as_view(template_name='compression_type.html'),name='compression_type'),
url('^document_list/(?P<pk>\d+)/compress$',CompressView.as_view(),name='compress'),
url('^document_list/*$',ListView.as_view(template_name='compression/document_list.html',model=Document),name='document_list'),
url('^document/add$',DocumentUploadView.as_view(),name='document_add'),
url('^document_list/(?P<pk>\d+)/{0,1}$',DetailView.as_view(template_name='compression/document.html',model=Document),name='document'),
url('^document_list/(?P<pk>\d+)/{0,1}/delete$',CompressDeleteView.as_view(),name='document_delete'),
#(r'^auth/$', getAuthUrl),
#(r'^verify/$', callback_handler),
#                       url(r'^oauth/',include('oauth_provider.urls'))
)
