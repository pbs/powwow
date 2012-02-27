from django.shortcuts import render_to_response

from powwow.apps.models import AppSettings


def index(request):
    return render_to_response('app.xml', {request: request})

def index_dev(request):
    return render_to_response('app_dev.xml', {request: request})
