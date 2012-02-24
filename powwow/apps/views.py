from django.shortcuts import render_to_response

from apps.models import AppSettings


def index(request):
    return render_to_response('app.xml')
