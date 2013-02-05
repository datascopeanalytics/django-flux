Here's the situation. You're on a website and you think to yourself,
"whoa, this site is gnarly! I'd really like to stay up to date with
this." You hesitate. Will you be inundated with irrelevant content on
Twitter, etc.?

Although this information is readily available and often a click or
two away, these additional clicks create an unnecessary barrier to
entry. The goal of ``flux`` is to make it possible to quickly
assess the utility of following a particular feed of content and
whether the `flux <http://en.wikipedia.org/wiki/Flux>`_ of relevant
content will be useful for you. Currently, ``flux`` supports:

* Twitter via `python-twitter <https://github.com/bear/python-twitter>`_
* RSS via `feedparser <http://packages.python.org/feedparser/>`_
* Facebook via `fbconsole <https://github.com/facebook/fbconsole>`_
* LinkedIn via `oauth2 <https://github.com/simplegeo/python-oauth2>`_

Quick start
===========

#. Install ``flux`` with `pip <http://www.pip-installer.org/en/latest/>`_::

    [shell]$ pip install django-flux

#. Add ``flux`` to the `INSTALLED_APPS
   <https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`_
   in `settings.py` of your django project::

    INSTALLED_APPS += ('flux', )

#. Run ``syncdb`` to create the necessary tables::

    [shell]$ python manage.py syncdb

#. Make sure the `admin is enabled
   <https://docs.djangoproject.com/en/dev/intro/tutorial02/#activate-the-admin-site>`_
   on your site and add accounts to monitor by visiting the admin page
   of your site (e.g., http://localhost:8000/admin/flux/account/add)

#. Run the ``update_flux`` management command::

    [shell]$ python manage.py update_flux

#. Use the ``flux_timeseries`` template tag on ``Account`` instances
   (``account`` below) in your templates::

    <link rel="stylesheet" href="{{STATIC_URL}}flux/css/timeseries.css" />

    {% load flux %}
    {% flux_timeseries account %}

   and you should see something like this:

   .. image:: https://github.com/datascopeanalytics/django-flux/raw/master/docs/basic_view.png
      :alt: default flux timeseries view
      :align: center

#. Customize the styling and layout by altering the CSS, and content
   accordingly or by taking advantage of any of the other ways of
   displaying the flux information:

Labels on mouseover with bars
-----------------------------

Optionally include labels for the bars with `d3.js <http://d3js.org>`_
by including the following in your templates::

    <link rel="stylesheet" href="{{STATIC_URL}}flux/css/timeseries.css" />
    <link rel="stylesheet" href="{{STATIC_URL}}flux/css/bar_mouseover_labels.css" />

    {% load flux %}
    {% flux_timeseries account %}

    <script src="//d3js.org/d3.v2.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script src="{{STATIC_URL}}flux/js/bar_mouseover_labels.js"></script>

and you should see something like this:

.. image:: https://github.com/datascopeanalytics/django-flux/raw/master/docs/bar_labelled.png
   :alt: labelled bars in the timeseries view
   :align: center

Sparklines
----------

Optionally include `sparklines
<http://en.wikipedia.org/wiki/Sparkline>`_ with `d3.js
<http://d3js.org>`_ by including the following in your templates::
  
    <link rel="stylesheet" href="{{STATIC_URL}}flux/css/timeseries.css" />
    <link rel="stylesheet" href="{{STATIC_URL}}flux/css/sparkline.css" />

    {% load flux %}
    {% flux_timeseries account %}

    <script src="//d3js.org/d3.v2.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script src="{{STATIC_URL}}flux/js/sparklines.js"></script>

and you should see something like this:

.. image:: https://github.com/datascopeanalytics/django-flux/raw/master/docs/sparkline.png
   :alt: sparkline view
   :align: center

Production usage
================

To have the Accounts monitored be continuously updated, add the
following line to your `crontab <http://en.wikipedia.org/wiki/Cron>`_
on your production server::

    0 0 * * * python /path/to/manage.py update_flux

Account configuration
=====================

Account.type="twitter"
----------------------

Account.name is the Twitter username (*e.g.*, for
http://twitter.com/DsAtweet, Account.name="DsAtweet").

No additional information is needed to access Twitter Accounts and
Account.other is ignored.

Account.type="rss"
------------------

Account.name is the full URL of the RSS feed you want to
track (*e.g.*, for http://datascopeanalytics.com/rss/,
Account.name="http://datascopeanalytics.com/rss/").

No additional information is needed to access Twitter Accounts and
Account.other is ignored.

Account.type="facebook"
-----------------------

Account.name is the name of the Facebook page that you want to track
(*e.g.*, for http://facebook.com/datascopeanalytics,
Account.name="datascopeanalytics")

The Account.other JSON must also include several attributes in order
to authenticate to the `Facebook API
<http://developers.facebook.com/>`_ using `fbconsole
<https://github.com/facebook/fbconsole>`_ with something like::

    {
        "app_id":"123456789012345",                          // [0-9]+
        "client_secret": "1234567890abcdef1234567890abcdef", // [0-9a-f]+
        "scope": ["read_stream"], 
        "email":"facebook.email@here.com", 
        "password": "this.is.your.facebook.password"
    }

Account.type="linkedin"
-----------------------

Account.name is the name of the LinkedIn company page that you want to
track (*e.g.*, for http://linkedin.com/company/datascope-analytics-llc,
Account.name="datascope-analytics-llc")

The Account.other JSON must also include several attributes in order
to authenticate to the `LinkedIn API
<https://developer.linkedin.com/documents/quick-start-guide>`_ with
something like::

    {
        "api_key": "1234567890ab",                      // [0-9a-f]+
        "api_secret": "1234567890ABCDEF",               // [0-9a-zA-Z]+
        "token":"12345678-90ab-cdef-1234-567890abcdef", // [0-9a-f\-]+
        "secret":"12345678-90ab-cdef-1234-567890abcdef" // [0-9a-f\-]+
    }

Contribute!
===========

#. Clone the code from `github
   <https://github.com/datascopeanalytics/django-flux>`_

#. Setup the virtualenv by following the instructions in
   `example_project/virtualenv_requirements.txt <https://raw.github.com/datascopeanalytics/django-flux/master/example_project/virtualenv_requirements.txt>`_

#. Edit, test, and share your code. See the `issues page
   <https://github.com/datascopeanalytics/django-flux/issues>`_ for
   inspiration and to coordinate with the community.

