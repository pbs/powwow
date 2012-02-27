from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('powwow.apps.views',
    url(r'^app.xml$', 'index', name='index'),
    url(r'^app.xml/dev$', 'index_dev', name='index_dev'),
    url(r'^app.xml/local$', 'local_dev', name='local_dev'),
    url(r'^confluence$', 'confluence', name='confluence'),
    url(r'^jira$', 'jira', name='jira'),
    url(r'^github$', 'github', name='github'),
)
