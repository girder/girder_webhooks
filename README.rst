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

Each configured hook may also contain a string-valued ``hmacKey`` field. If present, this key
will be used to generate and pass the ``Girder-Signature`` header. The value of this header is
the hex digest of the HMAC whose message is the request body, whose key is the ``hmacKey`` for the
webhook, and whose hash algorithm is SHA-256.

The request body is a JSON document containing the following fields:

* ``name`` (string): The name of the event.
* ``info``: The event info object related to this event.
* ``apiUrl`` (string): The URL of the REST API of the Girder instance sending the request.
* ``uid`` (string): A UUID for the request.
