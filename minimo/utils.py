
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.core import serializers
from django.utils import simplejson

import csv, codecs
import webodt
import pdb
import os


def export_csv(request, queryset, export_data, filter_by=None, file_name='exported_data.csv',
        object_id=None, not_available='n.a.', require_permission=None):
    '''
    Export objects from a queryset
    
    @param queryset: the queryset containing a list of objects
    @param export_data: a dictionary of the form 'path.to.data': 'Column Title'
    @param filter_by: filter the queryset by this column__condition and object_id
    @param file_name: the file name offered in the browser or a callable
    @param object_id: if file_name is callable and object_id is given, then the 
        file_name is determined by calling file_name(object_id)
    @param not_available: the default data if a given object in export_data 
        is not available
    @param require_permission: only user's havig the required permission can 
        access this view
        
    Example usage:
    'queryset': User.objects.all(),
    'filter_by': 'is_active',
    'object_id': 1,
    'export_data':  [
        ('username', 'User name'),
        ('get_full_name', 'Full name'),
        ('get_profile.some_profile_var', 'Some data'),
        ]
    '''
    if require_permission and not (request.user.is_authenticated() and 
                       request.user.has_perm(require_permission)):
        return redirect_to_login(request.path)
    queryset = queryset._clone()
    if filter_by and object_id:
        queryset = queryset.filter(**{'%s' % filter_by: object_id})
    
    def get_attr(object, attrs=None):
        if attrs == None or attrs == []:
            return object
        current = attrs.pop(0)
        try:
            return get_attr(callable(getattr(object, current)) and 
                        getattr(object, current)() or 
                        getattr(object, current), attrs)
        except (ObjectDoesNotExist, AttributeError):
            return not_available
    
    def stream_csv(data):
        sio = StringIO()
        writer = csv.writer(sio)
        writer.writerow(data)
        return sio.getvalue()
    
    def streaming_response_generator():
        yield codecs.BOM_UTF8
        yield stream_csv(zip(*export_data)[0])
        import django.db.models.query
        for item in queryset.iterator():
            
            row = []
            for attr in zip(*export_data)[1]:
                obj = get_attr(item, attr.split('.'))
                #pdb.set_trace()
                if callable(obj):
                    res = obj()
                else:
                    res = obj
                if isinstance(res, unicode) is True:
                    res = res.encode('utf-8')
                elif isinstance(res, dt.date) or isinstance(res, dt.datetime):
                    res=res.__str__()
                elif isinstance(res, django.db.models.query.QuerySet) is True:
                    elenco=''
                    for i in res:
                        elenco+=i.__unicode__()+", "
                    res=elenco
                elif isinstance(res, str) is False:
                    res = str(res)
                row.append(res)
            yield stream_csv(row)
    
    rsp = HttpResponse(streaming_response_generator(), 
                        mimetype='text/csv', 
                        content_type='text/csv; charset=utf-8')
    filename = object_id and callable(file_name) and file_name(object_id) or file_name
    rsp['Content-Disposition'] = 'attachment; filename=%s' % filename.encode('utf-8')
    return rsp

