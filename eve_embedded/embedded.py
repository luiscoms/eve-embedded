"""
Módulo para embarcar dados de outras apis.

Usage:

No Settings:

'authors': {
    'type': 'list',
    'maxlength': 15,
    'schema': {"type": "string", "data_relation": {"api": "http://api.rbs.com.br/authors", "embeddable": True}}
},

No application.py:

from apis_common import embedded

application = Eve()
embedded.install(application)

Depende do módulo validator.py

Funcionamento:

Monkey patch que altera o método build_response_document para incluir
dados de outros serviços.

"""

from eve.methods import common
from eve.utils import parse_request, config, debug_error_message
import importlib
import json
import logging
import requests

default_headers = {"Accept": "text/json"}

# hook
before_build_document = []

logger = logging.getLogger(__name__)


def new_resolve_embedded_fields(resource, req, document):
    embedded_fields = []
    if req.embedded:
        try:
            client_embedding = json.loads(req.embedded)
        except ValueError:
            abort(400, description=debug_error_message(
                'Unable to parse `embedded` clause'
            ))
        try:
            embedded_fields = [k for k, v in client_embedding.items()
                               if v == 1]
        except AttributeError:
            # We got something other than a dict
            abort(400, description=debug_error_message(
                'Unable to parse `embedded` clause'
            ))

    embedded_fields = list(
        set(config.DOMAIN[resource]['embedded_fields']) |
        set(embedded_fields))
    enabled_embedded_fields = []
    for field in embedded_fields:
        field_def = new_field_definition(resource, field, document)
        if type(field_def) is dict:
            if field_def.get('type') == 'list':
                field_def = field_def['schema']
            if 'data_relation' in field_def and \
                    field_def['data_relation'].get('embeddable'):
                enabled_embedded_fields.append(field)

    return enabled_embedded_fields


def new_field_definition2(resource, chained_fields):

    definition = config.DOMAIN[resource]
    subfields = chained_fields.split('.')

    for field in subfields:
        if field not in definition.get('schema', {}):
            if 'data_relation' in definition and 'resource' in definition['data_relation']:
                sub_resource = definition['data_relation']['resource']
                definition = config.DOMAIN[sub_resource]
            else:
                definition = {'schema': {}}

        if field not in definition['schema']:
            return {}
        definition = definition['schema'][field]
        field_type = definition.get('type')
        if field_type == 'list':
            definition = definition['schema']
        elif field_type == 'objectid':
            pass
    return definition


def new_field_definition(resource, chained_fields, document):
    definition = config.DOMAIN[resource]
    subfields = chained_fields.split('.')

    for field in subfields:
        try:
            definition = definition['schema'][field]
            if definition.get('type') in ('list', 'string')\
               and 'schema' in definition:
                definition = definition['schema']
            elif definition['type'] == 'vars_meta':
                try:
                    tmpl = importlib.import_module(
                        'classifications_api.vars_meta_templates.{}'
                        .format(document['vars_meta_template']))
                    definition = {'schema': tmpl.schema}
                except ImportError:
                    pass

        except KeyError:
            return None

    return definition


def get_content(resource, content_id, additional_embedded={}):
    if not resource.startswith('http'):
        resource = 'http://api.rbs.com.br/' + resource
    parms = {}
    if additional_embedded:
        parms['embedded'] = json.dumps(dict((x, 1) for x in additional_embedded))
    try:
        embedded_req = requests.get('{}/{}'.format(resource, content_id), headers=default_headers, params=parms)
        embedded_doc = embedded_req.json()
        if embedded_req.status_code != 200:
            raise Exception("Error getting doc: {} - {}".format(embedded_req.status_code, str(embedded_doc)))
        if embedded_doc.get('_links'):
            del embedded_doc['_links']
    except:
        logger.error("Erro ao carregar conteúdo: {}/{}".format(resource, content_id), exc_info=True)
        embedded_doc = None
    return embedded_doc


def embedded_document(reference, data_relation, field_name, additional_embedded={}):
    return get_content(data_relation['resource'], reference, additional_embedded)


def resolve_additional_embedded_documents(document, resource, embedded_fields):
    req = parse_request(resource)
    try:
        if req.embedded:
            extra_embedded = json.loads(req.embedded)
        else:
            extra_embedded = {}
    except ValueError:
        abort(400, description='Unable to parse `embedded` clause')
    extra_embedded = extra_embedded.keys()
    for field in new_resolve_embedded_fields(resource, req, document):
        field_extra_name = field + '.'
        field_extra_embedded = filter(lambda x: x.startswith(field_extra_name), extra_embedded)
        field_extra_embedded = map(lambda x: x.replace(field_extra_name, '', 1), field_extra_embedded)
        field_extra_embedded = list(field_extra_embedded)
        data_relation = new_field_definition(resource, field, document)['data_relation']
        getter = lambda ref: embedded_document(ref, data_relation, field, field_extra_embedded)
        fields_chain = field.split('.')
        last_field = fields_chain[-1]
        for subdocument in common.subdocuments(fields_chain[:-1], document=document, resource=resource):
            if last_field not in subdocument:
                continue
            if isinstance(subdocument[last_field], list):
                embedded_value = list(map(getter, subdocument[last_field]))
                embedded_value = [x for x in embedded_value if x is not None]
                subdocument[last_field] = embedded_value
            else:
                embedded_value = getter(subdocument[last_field])
                subdocument[last_field] = embedded_value


def install(app):
    original_build_response_document = common.build_response_document

    def new_build_response_document(document, resource, embedded_fields, latest_doc=None):
        for method in before_build_document:
            method(document, resource, embedded_fields, latest_doc)
        old_embedded_fields = filter(lambda x: new_field_definition(resource, x, None).get('data_relation').get('resource'), embedded_fields)
        old_embedded_fields = list(old_embedded_fields)
        new_embedded_fields = filter(lambda x: not new_field_definition(resource, x, None).get('data_relation').get('resource'), embedded_fields)
        new_embedded_fields = list(new_embedded_fields)
        result = original_build_response_document(document, resource, old_embedded_fields, latest_doc)
        resolve_additional_embedded_documents(document, resource, new_embedded_fields)
        return result

    common.field_definition = new_field_definition2
    common.build_response_document = new_build_response_document
    importlib.reload(importlib.import_module('eve.methods.get'))
