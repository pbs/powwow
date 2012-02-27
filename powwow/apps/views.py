import xmlrpclib

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings

from powwow.apps.models import AppSettings


def index(request):
    return render_to_response('app.xml')

def index_dev(request):
    return render_to_response('app_dev.xml')

def local_dev(request):
    return render_to_response('app_dev.html')

def confluence(request):
    spacekey = AppSettings.objects.get(name='conf_space')
    pagetitle = AppSettings.objects.get(name='conf_page')

    server = xmlrpclib.ServerProxy(settings.CONFLUENCE_API)
    token = server.confluence1.login(
            settings.CONFLUENCE_USER,
            settings.CONFLUENCE_PASS
    )

    page = server.confluence1.getPage(
            token,
            spacekey.content,
            pagetitle.content
    )
    if page is None:
       return HttpResponse("Could not find page "+spacekey+":"+pagetitle)

    return render_to_response('confluence.html', {'content': page['content']})

def jira(request):
    return render_to_response('jira.html')

def github(request):
    return render_to_response('github.html')
