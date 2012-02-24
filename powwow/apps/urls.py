from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('powwow.apps.views',
    url(r'^app.xml$', 'index', name='index'),
)
