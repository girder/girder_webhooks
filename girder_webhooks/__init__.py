import functools
import json
import jsonschema
import requests
from girder import events
from girder.exceptions import ValidationException
from girder.models.setting import Setting
from girder.plugin import GirderPlugin
from girder.utility import setting_utilities, JsonEncoder


_HOOKS = 'webhooks.hooks'
_HOOK_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'event': {
                'type': 'string'
            },
            'url': {
                'type': 'string'
            }
        },
        'required': ['event', 'url']
    }
}


@setting_utilities.validator(_HOOKS)
def validate(doc):
    try:
        jsonschema.validate(doc['value'], _HOOK_SCHEMA)
    except jsonschema.ValidationError as e:
        raise ValidationException('Invalid webhooks: ' + e.message)


def _emitHook(url, event):
    body = json.dumps({
        'name': event.name,
        'info': event.info
    }, cls=JsonEncoder)
    requests.post(url, data=body, headers={'Content-Type': 'application/json'})


class WebhooksPlugin(GirderPlugin):
    DISPLAY_NAME = 'Webhooks'

    def load(self, info):
        for hook in Setting().get(_HOOKS, ()):
            events.bind(
                hook['event'], 'webhook:%s:%s' % (hook['event'], hook['url']),
                functools.partial(_emitHook, url=hook['url']))

