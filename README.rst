Here's the situation. You're on a website that you think is pretty
cool and you think it may be worth following them on Twitter (or RSS,
Facebook, Google+, etc). You hesitate. Will you be inundated with
irrelevant content?

Although this information is readily available and often a click or
two away, these additional clicks create an unnecessary barrier to
entry. The goal of `flux` is to make it possible to quickly
assess the utility of following a particular feed of content and
whether the `flux <http://en.wikipedia.org/wiki/Flux>`_ of relevant
content will be useful for you. Currently, `flux` supports:

* Twitter
* RSS

Quick start
===========

#. Install `flux` with `pip <http://www.pip-installer.org/en/latest/>`_::

    $ pip install django-flux

#. Add `flux` to the `INSTALLED_APPS
   <https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`
   in `settings.py` of your django project::

    INSTALLED_APPS += ('flux', )

#. Add accounts to monitor by visiting the admin page of your site
   (likely http://localhost:8000/admin/flux/account/add)

#. Run the `update_flux` management command::

    $ python manage.py update_flux

#. TODO: UPDATE WHEN PRELIMINARY VIEW IS AVAILABLE

Production usage
================

TODO: EXPLAIN HOW TO INSTALL IN CRONTAB IN PRODUCTION ENVIRONMENTS

How it works
============

Most of these content streams (Twitter, RSS, etc) have open APIs that
make it possible to access their data in real time. The tricky bit is
that it is often slower to request this information from several
different APIs than it is to make a single request to a single
centralized server. So as to not decrease site performance,
django-flux provides the functionality to fetch and store this data
locally.

TODO: DESCRIBE MODELS

TODO: DESCRIBE MANAGEMENT COMMANDS

TODO: DESCRIBE TEMPLATE TAGS

Contribute!
===========

#. Clone the code from `github
   <https://github.com/deanmalmgren/django-flux>`_

#. Setup the virtualenv by following the instructions in
   example_project/virtualenv_requirements.txt

#. Edit, test, and share your code. 
