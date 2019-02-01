import functools
import hashlib
import hmac
import json
import jsonschema
import requests
import uuid
from girder import events
from girder.exceptions import ValidationException
from girder.models.setting import Setting
from girder.plugin import GirderPlugin
from girder.api.rest import getApiUrl
from girder.utility import setting_utilities, JsonEncoder


_HOOKS = 'webhooks.hooks'
_HOOK_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string'
            },
            'url': {
                'type': 'string'
            },
            'hmacKey': {
                'type': 'string'
            }
        },
        'required': ['name', 'url']
    }
}


@setting_utilities.validator(_HOOKS)
def validate(doc):
    try:
        jsonschema.validate(doc['value'], _HOOK_SCHEMA)
    except jsonschema.ValidationError as e:
        raise ValidationException('Invalid webhooks: ' + e.message)


def _emitHook(event, hook):
    body = json.dumps({
        'apiUrl': getApiUrl(),
        'name': event.name,
        'info': event.info,
        'uid': uuid.uuid4()
    }, cls=JsonEncoder)
    headers = {'Content-Type': 'application/json'}

    if 'hmacKey' in hook:
        headers['Girder-Signature'] = 'sha256=' + hmac.new(
            hook['hmacKey'].encode('utf8'), body, hashlib.sha256).hexdigest()

    # TODO this is blocking (because requests is blocking). We should do this asynchronously.
    requests.post(hook['url'], data=body, headers=headers)


class WebhooksPlugin(GirderPlugin):
    DISPLAY_NAME = 'Webhooks'

    def load(self, info):
        for hook in Setting().get(_HOOKS, ()):
            events.bind(
                hook['name'], 'webhook:%s:%s' % (hook['name'], hook['url']),
                functools.partial(_emitHook, hook=hook))
