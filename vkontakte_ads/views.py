# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from models import Layout, TargetingStats, Ad, Account, Targeting, Layout
from utils import JsonResponse

def ad_preview(request, ad_id):
    '''
    Return preview of ad without restriction tag for preventing output preview in iframes
    '''
    ad = Layout.objects.get(remote_id=ad_id)
    return HttpResponse(ad.preview)

@csrf_exempt
@login_required
def targeting_stats(request, ad_id=None):
    '''
    Return targeting audiency and recommended bid
    '''
    kwargs = dict([(k,v) for k,v in request.POST.items() if k[:6] in ['layout','target']])
    if 'account_id' in request.POST:
        try:
            account = Account.objects.get(id=request.POST['account_id'])
        except:
            pass
    elif ad_id:
        try:
            account = Ad.objects.get(id=ad_id).account
        except:
            pass

    stat = TargetingStats.remote.get(ad=Ad(account=account, **kwargs))
    response = stat.__dict__
    del response['_state']
    return JsonResponse(response)