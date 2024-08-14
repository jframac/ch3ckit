# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from random import randrange
from datetime import datetime

from faker import Faker  
fake = Faker()

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    data = []
    ports = []
    counter = 1
    for _ in range(200):
        dict = {
            'counter': counter,
            'ip': fake.ipv4_private(address_class='c'),
            'computer': fake.hostname(0),
            'capacity': randrange(100),
            'mac': fake.mac_address()
        }
        data.append(dict)
        counter += 1
    counter = 1
    for _ in range(20):
        dict = {
            'counter': counter,
            'port': fake.port_number(is_user=1, is_system=0),
            'times': randrange(1000)
        }
        ports.append(dict)
        counter += 1
    context['data'] = data
    context['ports'] = ports
    context['today'] = datetime.now()

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    context['today']= timezone.now() 
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
