# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext

import models

def account_index(request):
    """List all of the accounts
    """
    return render_to_response(
        "flux/account_index.html",
        {
            "accounts": models.Account.objects.iterator(),
        },
        context_instance=RequestContext(request),
    )

def account_detail(request, account_id):
    """Quick 'n dirty view to see an account detail and show the
    templatetag in action
    """
    return render_to_response(
        "flux/account_detail.html",
        {
            "account": models.Account.objects.get(pk=int(account_id)),
        },
        context_instance=RequestContext(request),
    )
