Here's the situation. You're on a website that you think is pretty
cool and you think it may be worth following them on Twitter (or RSS,
Facebook, Google+, etc). You hesitate. Will you be inundated with
irrelevant content?

Although this information is readily available and often a click or
two away, these additional clicks create an unnecessary barrier to
entry. The goal of ``flux`` is to make it possible to quickly
assess the utility of following a particular feed of content and
whether the `flux <http://en.wikipedia.org/wiki/Flux>`_ of relevant
content will be useful for you. Currently, ``flux`` supports:

* Twitter via `python-twitter <https://github.com/bear/python-twitter>`_
* RSS via `feedparser <http://packages.python.org/feedparser/>`_

Quick start
===========

#. Install ``flux`` with `pip <http://www.pip-installer.org/en/latest/>`_::

    [shell]$ pip install django-flux

#. Add ``flux`` to the `INSTALLED_APPS
   <https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`
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

    <link rel="stylesheet" href="{{STATIC_URL}}flux/css/flux_timeseries.css" />

    {% load flux %}
    {% flux_timeseries account %}

#. Customize the styling and layout by altering the CSS, and content accordingly

Production usage
================

To have the feeds monitored be continuously updated, add the following
line to your `crontab <http://en.wikipedia.org/wiki/Cron>`_::

    0 0 * * * /path/to/manage.py update_flux

Contribute!
===========

#. Clone the code from `github
   <https://github.com/deanmalmgren/django-flux>`_

#. Setup the virtualenv by following the instructions in
   example_project/virtualenv_requirements.txt

#. Edit, test, and share your code. See the `issues page
   <https://github.com/deanmalmgren/django-flux/issues>`_ for
   inspiration.

