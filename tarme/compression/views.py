# -*- coding: utf-8 -*-
import tarfile, zipfile
import os
import sys
from os import chdir, unlink
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.files import File

from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.base import TemplateView#, BaseDetailView

from django.http import HttpResponse


from compression.models import Document, CompressedDocument
from compression.forms import DocumentForm, CompressForm

from tarme.settings import ROOT_DIR,MEDIA_ROOT


#

#


cKey = 'GtqjjxowolGUSWI6JYCi0ZHqQcigxelL'
cSecret = 'b2nB2wdIAEj4pGGTTuunY4B9qewIiQ5I3RKcjdE0PgX6AJUX'

import my_oauth
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.template.loader import get_template


import urlparse
import oauth2 as oauth
import requests

request_token_url = 'https://api.copy.com/oauth/request'
callback_url = 'http://localhost:8000/verify'
consumer = oauth.Consumer(key=cKey,secret=cSecret)
oauth_request = oauth.Request.from_consumer_and_token(consumer,parameters={'oauth_callback':callback_url},http_url=request_token_url)
oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(),consumer,None)

response = requests.get(request_token_url,headers=oauth_request.to_header())
request_token = dict(urlparse.parse_qsl(response.content))


def getRequestURL(request):
	request_token_url = 'https://api.copy.com/oauth/request'
	callback_url = 'http://localhost:8000/verify'
	consumer = oauth.Consumer(key=cKey,secret=cSecret)
	oauth_request = oauth.Request.from_consumer_and_token(consumer,parameters={'oauth_callback':callback_url},http_url=request_token_url)
	oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(),consumer,None)
	
	response = requests.get(request_token_url,headers=oauth_request.to_header())

	request_token = dict(urlparse.parse_qsl(response.content))
	theTemplate = get_template("auth.html")
	resp = theTemplate.render(Context({'authUrl': request_token}))
	return HttpResponse(resp)


def getAuthUrl(request):
	s = my_oauth.get_authorization_url("https://api.twitter.com/oauth/request_token",
	"https://api.twitter.com/oauth/authorize",
	"http://localhost:8000/verify") # change this to a real view
        #s= {}
	request.session["request_token"] = my_oauth.requestToken
	request.session["request_token_secret"] = my_oauth.requestTokenSecret
	theTemplate = get_template("auth.html")
	resp = theTemplate.render(Context({"authUrl" : s}))
	return HttpResponse(resp)

#class AuthURLView(TemplateView):
    

def callback_handler(request):
	s = request.GET["oauth_verifier"]
	r = request.session["request_token"]
	rs = request.session["request_token_secret"]
	my_oauth.get_access_token("https://api.twitter.com/oauth/access_token",
	r, rs, s)
	request.session["access_token"] = my_oauth.accessToken
	request.session["access_token_secret"] = my_oauth.accessTokenSecret
	theTemplate = get_template("verify.html")
	resp = theTemplate.render(Context())
	return HttpResponse(resp)


'''
def tweet(request):
	theTemplate = get_template("tweet.txt")
	resp = theTemplate.render(RequestContext(request,
	{"accessToken" : request.session.get("access_token", ""),
	"accessTokenSecret" : request.session.get("access_token_secret", "")}))
	return HttpResponse(resp)
'''

'''
def update(request):
	my_oauth.set_access_token(request.POST["access"], request.POST["secret"])
	s = my_oauth.get_api_response("https://api.twitter.com/1/statuses/update.json",
	"POST", {"status" : request.POST.get("status")})
	theTemplate = get_template("update.txt")
	resp = theTemplate.render(Context({"dump" : s}))
	return HttpResponse(resp)
'''




class SuccessView(TemplateView):
    template_name = 'success.html'


class CompressDeleteView(DeleteView):
        model = Document
        success_url = reverse_lazy('document_list')
'''
class FileResponseMixin(object):
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content-type'] = 'application/'

class DownloadView()
   
'''
 
class CompressView(FormView):
    template_name = 'compress.html'
    model = Document
    form_class = CompressForm
    def get_success_url(self, **kwargs):
        print(self.kwargs['pk'])
        return '/document_list/{pk}'.format(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):        

        form = CompressForm(request.POST)
        if self.form_valid(form):
            # compression_type = request.POST['compression_type']
            document = Document.objects.get(pk=kwargs['pk'])
            #print(MEDIA_ROOT+'/'+document.doc.name[0:document.doc.name.rfind('/')+1])
            fullpath = MEDIA_ROOT+'/'+document.doc.name
            chdir(MEDIA_ROOT+'/'+document.doc.name[0:document.doc.name.rfind('/')+1])
            the_types = ['tar.gz', 'tar.bz2', 'gzip', 'zip']
            size_by_filename = {}
            for the_type in the_types:
                compression_type = the_type
                tarType = 'gz'
                if compression_type == 'tar.gz':
                    tarType = 'gz'
                elif compression_type == 'tar.bz2':
                    tarType = 'bz2'
                elif compression_type == 'gzip':
                    tarType = 'gz'
                elif compression_type == 'zip':
                    tarType = ''
                    doZip = True
                tarfilepath = '{}.{}'.format(fullpath,compression_type)
                if tarType:
                        if not os.path.exists(tarfilepath):
                                tar = tarfile.open(tarfilepath,'w:{tType}'.format(tType=tarType))
                                tar.add(fullpath)
                                tar.close()

                elif doZip:
                    zFile = zipfile.ZipFile(tarfilepath,'w')
                    zFile.write(fullpath)
                    zFile.close()
                    if not os.path.exists(tarfilepath):
                            with open(tarfilepath,'r') as f:
                                    myfile = File(f)
                                    cDoc = CompressedDocument()
                                    cDoc.compression_type = compression_type
                                    cDoc.compressed_doc.save(tarfilepath+'.'+compression_type,myfile)
                                    cDoc.save()
                                    document.compressed_docs.add(cDoc)
                                    document.save()
                                    unlink(tarfilepath)

                chdir(ROOT_DIR)
                if os.path.exists(tarfilepath):
                        with open(tarfilepath,'r') as f:
                                myfile = File(f)
                                cDoc = CompressedDocument()
                                cDoc.compression_type = compression_type
                                cDoc.compressed_doc.save(document.doc.name+'.'+compression_type,myfile)
                                cDoc.save()
                                size_by_filename[cDoc] = cDoc.compressed_doc.size
                                document.compressed_docs.add(cDoc)
                                document.save()
                                unlink(tarfilepath)
            largest_size = min(size_by_filename.itervalues())
            doc_to_keep = None
            for the_doc, the_size in size_by_filename.iteritems():
                if the_size == largest_size:
                    doc_to_keep = the_doc
            docs_to_remove = []
            for a_c_doc in document.compressed_docs.all():
                if not a_c_doc == doc_to_keep:
                    docs_to_remove.append(a_c_doc)
            map(document.compressed_docs.remove, docs_to_remove)
            document.save()
            return super(CompressView, self).post(request,*args,**kwargs)

    
    
    def get_context_data(self, **kwargs):
        context = super(CompressView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context
    



class DocumentUploadView(FormView):
    template_name = 'compression/document_add.html'
    form_class = DocumentForm
    model = Document
    success_url = '/document_list/'

    def post(self, request, *args, **kwargs):        
        form = DocumentForm(request.POST,request.FILES)
        if self.form_valid(form):
            newDocument = Document(doc = request.FILES['document'])
            newDocument.save()
            return super(DocumentUploadView, self).post(request,*args,**kwargs)

