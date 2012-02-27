import xmlrpclib
import urllib
import urllib2
import json

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.core.context_processors import csrf

from powwow.apps.models import AppSettings


def index(request):
    static_url = settings.STATIC_URL
    return render_to_response('app.xml', {'static_url': static_url})


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

    if request.method == 'POST':
       for key,value in request.POST.iteritems():
           if key == 'notes':
               page['content'] = value
               server.confluence1.storePage(token, page)

    params = {'content': page['content']}
    params.update(csrf(request))
    return render_to_response('confluence.html', params)


def jira(request):
    session = login()
    # TODO: date should not be hardcoded!
    jql = "project = UNICORN AND updated >= 2012-02-24 order by updated"
    url = ("%s/search?jql=%s&startAt=0&maxResults=10&JSESSIONID=%s"
           % (settings.JIRA_API, urllib2.quote(jql), session["JSESSIONID"]))

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=%s' % session["JSESSIONID"]))
    response = opener.open(url)

    issues = json.loads(response.read())
    print "*** %s" % issues
    return render_to_response('jira.html', {'issues': issues.get("issues")})
    
def jira_issue(request):
    return json.dumps(get_issue("UNICORN-3646"))


def github(request):
    return render_to_response('github.html')

def get_issue(issue_id):
    req = urllib2.Request("%s/issue/%s" % (settings.JIRA_API, issue_id))
    response = urllib2.urlopen(req)
    return json.loads(response.read())
    
def login():
    url = "%s/session" % settings.JIRA_AUTH
    values = {"username": settings.CONFLUENCE_USER, "password": settings.CONFLUENCE_PASS}
    data = json.dumps(values)
    headers = {'Content-type': 'application/json'}
    req = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e
        return {}
    session = json.loads(response.read())
    print "*** session = %s" % session
    return { session["session"]["name"]: session["session"]["value"] }
