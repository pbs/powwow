from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('powwow.apps.views',
    url(r'^app.xml$', 'index', name='index'),
    url(r'^app.xml/dev$', 'index_dev', name='index_dev'),
    url(r'^app.xml/local$', 'local_dev', name='local_dev'),
    url(r'^confluence/page/$', 'confluence', name='confluence'),
    url(r'^jira/page/$', 'jira', name='jira'),
    url(r'^jira/issue/$', 'jira_issue', name='jira_issue'),
    url(r'^github/page/$', 'github', name='github'),
)
