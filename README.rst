========================================
CCTV for SAM V1 with RabbitMQ and Docker
========================================


.. image:: https://img.shields.io/pypi/v/events.svg
        :target: https://pypi.python.org/pypi/events

.. image:: https://img.shields.io/travis/manqx/events.svg
        :target: https://travis-ci.org/manqx/events

.. image:: https://readthedocs.org/projects/events/badge/?version=latest
        :target: https://events.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




CCTV for SAM V1 with RabbitMQ and Docker


* Free software: MIT license
* Documentation: https://events.readthedocs.io.


Features
--------
* TODO

Usage
--------
* http post :8088/auth username=admin password=admin
* export token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE1MjQ4MTExOTR9.M44IxJGfRBvZsextbtvWYpA0HNNo13-MS47FC4bMc78
* http -A jwt --auth $token :8088/v1/cables

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
