Here's the situation. You're on a website that you think is pretty
cool and you think it may be worth following them on Twitter (or RSS,
Facebook, Google+, etc). You hesitate. Will you be inundated with
irrelevant content?

Although this information is readily available and often a click or
two away, these additional clicks create an unnecessary barrier to
entry. The goal of django-flux is to make it possible to quickly
assess the utility of following a particular feed of content and
whether the `flux <http://en.wikipedia.org/wiki/Flux>`_ of relevant
content will be useful for you.

Quick start
===========

TODO: FILL THIS IN WHEN pip IS WORKING


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

Contribute!
===========

TODO: DESCRIBE HOW TO EXTEND django-flux
