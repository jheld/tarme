from oauth import *
import urllib #for url-encode
import urllib2 #for getting and receiving data from server
import time #Unix timestamp
import hmac #for signing
import hashlib #for signing
import random #For nonce generation
import json
import base64 #For conversion of hmac hash from bytes to human-readable string


consumerKey = 'GtqjjxowolGUSWI6JYCi0ZHqQcigxelL'
consumerSecret = 'b2nB2wdIAEj4pGGTTuunY4B9qewIiQ5I3RKcjdE0PgX6AJUX'
accessToken = ""
accessTokenSecret = ""
requestToken = ""
requestTokenSecret = ""


def setConsumerCreds(ckey, csecret):
	global consumerKey
	global consumerSecret
	consumerKey = ckey
	consumerSecret = csecret

def set_access_token(key, secret):
	global accessToken
	global accessTokenSecret
	accessToken = key
	accessTokenSecret = secret



def _get_base_string(resourceUrl, values, method="POST"):
	# In the format METHOD&encoded(resource)&parameter=value&parameter=value&...
	baseString = method + "&" + url_encode(resourceUrl) + "&"
	#The parameters and values should be sorted by name, and then by value.
	sortedKeys = sorted(values.keys())
	#We use sorted() as opposed to values.keys().sort() so we don't modify the original collection.


def _add_oauth_parameters(parameters, addAccessToken = True):
	parameters["oauth_consumer_key"] = consumerKey
	if (addAccessToken):
		parameters["oauth_token"] = accessToken
	parameters["oauth_version"] = "1.0"
	#Nonce in our case is a numeric value, but we need
	#to cast it to a string so it can be url-encoded.
	parameters["oauth_nonce"] = str(_get_nonce())
	parameters["oauth_timestamp"] = str(_get_timestamp())

	parameters["oauth_signature_method"] = "HMAC-SHA1"


def _get_nonce():
	# Simply choose a number between 1 and 999,999,999
	r = random.randint(1, 999999999)
	return r



def _get_timestamp():
	return int(time.time())




def _get_signature(signingKey, stringToHash):
    hmacAlg = hmac.HMAC(signingKey, stringToHash, hashlib.sha1)
    return base64.b64encode(hmacAlg.digest())


def url_encode(data):
	return urllib.quote(data, "")

def _build_oauth_headers(parameters):
	header = "OAuth "
	sortedKeys = sorted(parameters.keys()) #although not necessary
	for i in range(len(sortedKeys)):
		header = header + url_encode(sortedKeys[i]) + "=\"" + url_encode(parameters[sortedKeys[i]]) + "\""
		if i < len(sortedKeys) - 1:
			header = header + ","
	print(header)
	return header

def get_authorization_url(resourceUrl, endpointUrl, callbackUrl):
        global requestToken
	oauthParameters = {}
        _add_oauth_parameters(oauthParameters, False)
        if 'access' in resourceUrl:
            oauthParameters['X-Api-Version'] = '1'
            oauthParameters['Accept'] = 'application/json'
        #scope = json.dumps([{'profile':{'read':True,'write':True}},{'email':{'read':True}},{'inbox':{'read':False}},{'links':{'read':False,'write':False}},{'filesystem':{'read':True,'write':True}}])
        scope = [{'profile':{'read':True,'write':True}},{'email':{'read':True}},{'inbox':{'read':False}},{'links':{'read':False,'write':False}},{'filesystem':{'read':True,'write':True}}]
        #oauthParameters['scope'] = scope

	oauthParameters["oauth_callback"] = callbackUrl
	resourceUrl = resourceUrl.upper()
        baseString = _get_base_string(resourceUrl, oauthParameters)
	signingKey = consumerSecret + "&"
        oauthParameters["oauth_signature"] = str(_get_signature(signingKey, baseString))
        oauthParameters['oauth_signature'] = oauthParameters['oauth_signature'][1:]
        headers = _build_oauth_headers(oauthParameters)
        #parameters = {'scope':scope,'oauth_signature':_get_signature(signingKey, baseString)}
	#httpRequest = urllib2.Request(resourceUrl, urllib.urlencode(parameters))
        httpRequest = urllib2.Request(resourceUrl)
	httpRequest.add_header("Authorization", headers)
        print(httpRequest.headers)
        try:
		httpResponse = urllib2.urlopen(httpRequest)
	except urllib2.HTTPError, e:
		return "Response: %s" % e.read()

	responseData = httpResponse.read()
        responseParameters = responseData.split('&') #gives is a list with each parameter / value pair
	for s in responseParameters: #these are strings, so we're iterating over a list of strings.
		if s.find("oauth_token_secret")  -1 and len(s)>=2:
			requestTokenSecret = s.split('=')[1]
		else:
			if s.find("oauth_token")  -1 and len(s)>=2:
				requestToken = s.split('=')[1]

	return endpointUrl + "?oauth_token=" + requestToken

def get_access_token(resourceUrl, requestTok, requestTokSecret, oauth_verifier):
	global requestToken
	global requestTokenSecret
	global accessToken
	global accessTokenSecret
	requestToken = requestTok
	requestTokenSecret = requestTokSecret
	oauthParameters = {"oauth_verifier" : oauth_verifier, "oauth_token" : requestToken}
	_add_oauth_parameters(oauthParameters, False)
	baseString = _get_base_string(resourceUrl, oauthParameters)
        signingKey = consumerSecret + "&" + requestTokenSecret
	oauthParameters["oauth_signature"] = _get_signature(signingKey, baseString)
	header = _build_oauth_headers(oauthParameters)
	httpRequest = urllib2.Request(resourceUrl)
	httpRequest.add_header("Authorization", header)
	httpResponse = urllib2.urlopen(httpRequest)
	responseParameters = httpResponse.read().split('&')
	for s in responseParameters:
		if s.find("oauth_token_secret")  -1:
			accessTokenSecret = s.split('=')[1]
		else:
			if s.find("oauth_token")  -1:
				accessToken = s.split('=')[1]




def get_api_response(resourceUrl, method = "POST", parameters = {}):
	_add_oauth_parameters(parameters)
	baseString = _get_base_string(resourceUrl, parameters, method)
	signingKey = consumerSecret + "&" + accessTokenSecret
	parameters["oauth_signature"] = _get_signature(signingKey, baseString)
	parameters2 = {}
	for s in sorted(parameters.keys()):
		if s.find("oauth_") == -1:
			parameters2[s] = parameters[s]
			del parameters[s]
	header = _build_oauth_headers(parameters)
	httpRequest = urllib2.Request(resourceUrl, urllib.urlencode(parameters2))
	httpRequest.add_header("Authorization" , header)
	httpResponse = urllib2.urlopen(httpRequest)
	respStr = httpResponse.read()

