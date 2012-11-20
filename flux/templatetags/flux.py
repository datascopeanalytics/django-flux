
from django import template

register = template.Library()

@register.inclusion_tag('flux/timeseries.html')
def flux_timeseries(account):
    """This `inclusion tag
    <https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#inclusion-tags>`_
    is used to render the flux/timeseries.html template. 
    """
    return {
        "timeseries": account.get_timeseries(),
    }
