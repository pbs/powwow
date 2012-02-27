from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('powwow.apps.views',
    url(r'^app.xml$', 'index', name='index'),
    url(r'^app_dev.xml$', 'index_dev', name='index_dev'),
)
