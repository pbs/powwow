import xmlrpclib
import urllib2
import json
import datetime
import functools

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from powwow.apps.models import AppSettings


def index(request):
    return render_to_response('app.xml', {
        'url_static': settings.STATIC_URL,
        'app_url': settings.APP_URL,
    })


def index_dev(request):
    return render_to_response('app_dev.xml')


def local_dev(request):
    return render_to_response('app_dev.html')

@csrf_exempt
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
        response_text = "Could not find page %s:%s" % (spacekey, pagetitle)
        return add_cors_headers(HttpResponse(response_text))

    if request.method == 'POST':
        for key,value in request.POST.iteritems():
            if key == 'notes':
                page['content'] = value
                server.confluence1.storePage(token, page)
        return add_cors_headers(HttpResponse("Saved"))

    params = {'content': page['content']}
    response = render_to_response('confluence.html', params)
    response = add_cors_headers(response)
    return response


def jira(request):
    project = AppSettings.objects.get(name='jira_project')
    session = jira_login()

    #TODO the number of days back should be configurable
    date = datetime.datetime.now() - datetime.timedelta(days=7)
    date = date.strftime("%Y-%m-%d")

    jql = "project = %s AND updated >= %s order by updated" %(
            project.content, date
        )
    url = ("%s/search?jql=%s&startAt=0&maxResults=15&JSESSIONID=%s"
           % (settings.JIRA_API, urllib2.quote(jql), session["JSESSIONID"]))

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=%s'
            % session["JSESSIONID"]))
    response = opener.open(url)

    issues = json.loads(response.read())

    issues_details = [
        jira_issue(issue["key"], session) for issue in issues.get("issues")
    ]

    response = render_to_response('jira.html', {'issues': issues_details})
    response = add_cors_headers(response)
    return response


@csrf_exempt
def jira_find_issue(request):
    if request.method == 'POST':
        project = AppSettings.objects.get(name='jira_project')
        for key,value in request.POST.iteritems():
            if key == 'issue':
                issue = value.strip()

        issue_info = jira_issue(project.content + '-' + issue)
        if issue_info is None:
            return add_cors_headers(HttpResponse("The issue you are looking \
                    for does not exist in the current project."))

        response = render_to_response('jira_issue.html', {'issue': issue_info})
        response = add_cors_headers(response)
        return response
    else:
        return add_cors_headers(HttpResponse("You did not send any value to \
                search for."))


def jira_issue(issue_id, session=None):
    if session is None:
        session = jira_login()

    url = "%s/issue/%s" % (settings.JIRA_API, issue_id)

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=%s'
            % session["JSESSIONID"]))
    try:
        response = opener.open(url)
    except Exception:
        return None

    issue = json.loads(response.read())
    issue["browse_url"] = "%s/%s" %(settings.JIRA_BROWSE_URL,issue.get("key"))
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
    project = AppSettings.objects.get(name='github_project')

    url = '%s/repos/%s/%s/commits' % (
            settings.GITHUB_API, settings.GITHUB_USER, project.content
        )
    opener = urllib2.build_opener()
    try:
        res = opener.open(url)
    except Exception:
        return add_cors_headers(HttpResponse("Error trying to access GitHub!"))

    commits = json.loads(res.read())

    params = {'commits': commits, 'project': project.content,
            'user':settings.GITHUB_USER}
    response = render_to_response('github.html', params)
    response = add_cors_headers(response)
    return response


def add_cors_headers(response):
    response['Access-Control-Allow-Origin'] = settings.ALLOWED_ORIGIN
    response['Access-Control-Allow-Methods'] = 'POST, GET'
    return response
