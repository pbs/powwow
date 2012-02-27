import xmlrpclib
import urllib
import urllib2
import json
import datetime
import functools

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.core.context_processors import csrf

from powwow.apps.models import AppSettings


def index(request):
    url_static = settings.STATIC_URL
    return render_to_response('app.xml', {'url_static': url_static})


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

    response = render_to_response('confluence.html', params)
    response = add_cors_headers(response)
    return response


def jira(request):
    project = AppSettings.objects.get(name='jira_project')
    session = jira_login()

    date = datetime.datetime.now() - datetime.timedelta(days=7)
    date = date.strftime("%Y-%m-%d")

    jql = "project = %s AND updated >= %s order by updated" % \
            (project.content, date)
    url = ("%s/search?jql=%s&startAt=0&maxResults=10&JSESSIONID=%s"
           % (settings.JIRA_API, urllib2.quote(jql), session["JSESSIONID"]))

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=%s' % \
            session["JSESSIONID"]))
    response = opener.open(url)

    issues = json.loads(response.read())

    issues_details = [
        jira_issue(issue["key"], session) for issue in issues.get("issues")
    ]

    response = render_to_response('jira.html', {'issues': issues_details})
    response = add_cors_headers(response)
    return response


def jira_issue(issue_id, session):
    url = "%s/issue/%s" % (settings.JIRA_API, issue_id)

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=%s' % \
            session["JSESSIONID"]))
    response = opener.open(url)

    issue = json.loads(response.read())
    issue["browse_url"] = "%s/%s" % (settings.JIRA_BROWSE_URL, \
            issue.get("key"))
    return issue


def jira_login():
    url = "%s/session" % settings.JIRA_AUTH
    values = {"username": settings.JIRA_USER, "password": settings.JIRA_PASS}
    data = json.dumps(values)
    headers = {'Content-type': 'application/json'}
    req = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        return {}
    session = json.loads(response.read())
    return { session["session"]["name"]: session["session"]["value"] }


def github(request):
    response = render_to_response('github.html')
    response = add_cors_headers(response)
    return response


def add_cors_headers(response):
    response['Access-Control-Allow-Origin'] = settings.ALLOWED_ORIGIN
    response['Access-Control-Allow-Methods'] = 'POST, GET'
    return response
