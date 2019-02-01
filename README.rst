========
Webhooks
========

Webhooks triggered by Girder events

Usage
-----

To configure webhooks, set the ``webhooks.hooks`` setting to a JSON Array in which each
element is an Object with two keys: ``name`` and ``url``. The ``name`` field is a string,
the name of the Girder event that will trigger the hook. The ``url`` field is the URL that will
be sent an HTTP POST request whenever that event is triggered.

The request body is a JSON document containing two fields, ``name`` and ``info``. The ``name``
field is the event name, and the ``info`` is the JSON-encoded event info.

These webhooks are not authenticated in any way in this barebones implementation. HMAC signing would
be a good next feature to add.
