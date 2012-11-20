from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.account_index, name="account_index"),
    url(r'^(?P<account_id>\d+)', views.account_detail, name='account_detail'),
)
