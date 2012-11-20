
from django import template

register = template.Library()

@register.inclusion_tag('flux/timeseries.html', takes_context=True)
def flux_timeseries(context, account):
    """This `inclusion tag
    <https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#inclusion-tags>`_
    is used to render the flux/timeseries.html template. This needs to
    pass STATIC_URL and MEDIA_URL from the context; see `this
    <http://squeeville.com/2009/01/27/django-templatetag-requestcontext-and-inclusion_tag/>`_
    for details.
    """

    return {
        "STATIC_URL": context["STATIC_URL"],
        "MEDIA_URL": context["MEDIA_URL"],
        "account": account,
        "timeseries": account.get_timeseries(),
        "mean_label_template": account.get_mean_label_template(),
    }
