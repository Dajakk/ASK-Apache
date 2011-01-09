from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response

from Parser.parser import *
from forms import *

import datetime

def hello(request):
	return HttpResponse( "Hello world" )

def current_datetime(request):
	current_date = datetime.datetime.now( )
	return render_to_response( 'current_datetime.html', locals( ) )

def hours_ahead(request, offset):
	try:
		offset = int( offset )
	except ValueError:
		raise Http404( )
	dt = datetime.datetime.now( ) + datetime.timedelta( hours=offset )
	html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
	return HttpResponse( html )

def show_virtual_hosts(request):
	virtualHost = VirtualHost( )
	virtualHost.parse( "/home/Dajakk/Pobrane/Nauka/Administracja/administracja/src/default" )
	print len( virtualHost.nodes )
	return render_to_response( 'current_datetime.html', locals( ) )

def edit_virtual_host(request, virtualHostId):
	virtualHost = VirtualHost( )
	return render_to_response( 'editVirtualHost.html', locals( ) )

def edit_node(request, nodeId):
	try:
		nodeId = int( nodeId )
	except ValueError:
		raise Http404( )

	virtualHost = VirtualHost( )
	#virtualHost.parse( "/etc/httpd/conf/httpd.conf" )
	virtualHost.parse( "/home/Dajakk/Pobrane/Nauka/Administracja/administracja/src/default" )
	if nodeId > len( virtualHost.nodes ):
		raise Http404( )

	if request.method == 'POST': # If the form has been submitted...
		form = NodeForm( request.POST ) # A form bound to the POST data
		if form.is_valid( ): # All validation rules pass
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			cc_myself = form.cleaned_data['cc_myself']

			recipients = ['info@example.com']
			if cc_myself:
				recipients.append( sender )

			from django.core.mail import send_mail

			send_mail( subject, message, sender, recipients )
			return HttpResponseRedirect( '/thanks/' ) # Redirect after POST
	else:
		node = virtualHost.nodes[nodeId]
		data = {'subject': 'hello',
				'message': 'Hi there',
				'sender': 'foo@example.com',
				'cc_myself': True}

		form = NodeForm( data )
	return render_to_response( 'editNode.html', locals( ) )