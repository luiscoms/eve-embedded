import json
from pprint import pprint

import httpretty

from tests import TestBase  # noqa: E402


class TestEveEmbedded(TestBase):
    def test_api(self):
        self.app.debug = True
        r = self.test_client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_resource(self):
        self.app.debug = True
        r = self.test_client.get('/people')
        self.assertEqual(r.status_code, 200)

    def test_json(self):
        self.app.debug = True
        r = self.test_client.get('/people')
        s = r.get_data().decode('utf-8')  # raises UnicodeError
        j = json.loads(s)  # raises ValueError
        # pprint(j)

    # def notest_doc_is_dict(self):
    def test_embedded_relations(self):
        doc = self.test_client\
            .get('/people?embedded={"relations.relation":1}')\
            .get_data()\
            .decode('utf-8')

        j = json.loads(doc)
        print("--ls--"*10)
        pprint(j)
        self.assertIn('_items', doc)
        # self.assertIsInstance(doc, dict)

    @httpretty.activate
    def test_embedded_rest_relations(self):
        httpretty.disable()
        print("!!ls!!"*10)
        expected = self.test_client\
                       .get('/people')\
                       .get_data()\
                       .decode('utf-8')
        expected_json = json.loads(expected)
        pprint(expected_json)

        httpretty.enable()
        import re
        httpretty.register_uri(
            httpretty.GET,
            re.compile("http://myapi.com/(.*)"),
            body="{}",
        )
        httpretty.register_uri(httpretty.GET,
                               'http://myapi.com/people?embedded={"rest_relations.relation":1}',
                               content_type="application/json",
                               body=expected)
        print("register http://myapi.com/people/54f112defba522406c9cc209", type(json.dumps(expected_json.get('_items')[0])))
        httpretty.register_uri(httpretty.GET,
                               'http://myapi.com/people/54f112defba522406c9cc209',
                               content_type="application/json",
                               body=json.dumps(expected_json.get('_items')[0]))
        httpretty.register_uri(httpretty.GET,
                               'http://myapi.com/people/585a8be8f0983235bf0f95ed',
                               content_type="application/json",
                               body=json.dumps(expected_json.get('_items')[1]))

        doc = self.test_client \
            .get('/people?embedded={"rest_relations.relation":1}') \
            .get_data() \
            .decode('utf-8')

        print(">>> last_request")
        pprint(httpretty.last_request().body)
        print("<<< last_request")

        response_json = json.loads(doc)
        print("--mocked--" * 10)
        pprint(response_json)

        self.assertIn('_items', doc)
        self.assertEqual(expected_json, response_json)
        # self.assertIsInstance(doc, dict)

        # httpretty.disable()
        # httpretty.reset()

    def notest_info(self):
        doc = self.swagger_doc

        self.assertIn('info', doc)
        self.assertIn('title', doc['info'])
        self.assertTrue(isinstance(doc['info']['title'], u''.__class__))
        self.assertIn('version', doc['info'])
        self.assertTrue(isinstance(doc['info']['version'], u''.__class__))

    def notest_paths(self):
        doc = self.swagger_doc
        url = self.domain['people']['url']
        item_title = self.domain['people']['item_title']

        self.assertIn('paths', doc)
        self.assertIsInstance(doc['paths'], dict)
        self.assertIn('/'+url, doc['paths'])
        self.assertIn('/%s/{%sId}' % (url, item_title.lower()), doc['paths'])

    def notest_definitions(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']

        self.assertIn('definitions', doc)
        self.assertIsInstance(doc['definitions'], dict)
        self.assertIn(item_title, doc['definitions'])
        self.assertIn('properties', doc['definitions'][item_title])
        self.assertEqual(
            set(doc['definitions'][item_title]['properties'].keys()),
            set(['name', 'job', '_id', 'relations']))

    def notest_parameters_people(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']
        lookup_field = self.domain['people']['item_lookup_field']

        self.assertIn('parameters', doc)
        self.assertIn(item_title+'_'+lookup_field, doc['parameters'])

    def notest_resource_description(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']

        self.assertEqual('the people resource',
                         doc['definitions'][item_title]['description'])

    def notest_field_description(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']
        props = doc['definitions'][item_title]['properties']

        self.assertEqual('the last name of the person',
                         props['name']['description'])

    def notest_disabled_resource(self):
        doc = self.swagger_doc
        url = self.domain['disabled_resource']['url']
        item_title = self.domain['disabled_resource']['item_title']
        lookup_field = self.domain['disabled_resource']['item_lookup_field']

        self.assertNotIn('/'+url, doc['paths'])
        self.assertNotIn('/%s/{%sId}' % (url, item_title.lower()),
                         doc['paths'])
        self.assertNotIn(item_title, doc['definitions'])
        self.assertNotIn(item_title+'_'+lookup_field, doc['parameters'])

    def notest_data_relation_source_field(self):
        doc = self.swagger_doc

        source_field = self.domain['people']['item_title']+'_job'
        self.assertIn(source_field, doc['definitions'])

    def notest_reference_to_data_relation_source_field(self):
        doc = self.swagger_doc
        people_it = self.domain['people']['item_title']
        people_props = doc['definitions'][people_it]['properties']
        dr_1_it = self.domain['dr_resource_1']['item_title']
        dr_1_props = doc['definitions'][dr_1_it]['properties']
        key = people_it + '_job'

        self.assertIn('$ref', people_props['job'])
        self.assertEqual('#/definitions/%s' % key,
                         people_props['job']['$ref'])
        self.assertIn(key, doc['definitions'])

        self.assertIn('$ref', dr_1_props['copied_field_with_description'])
        self.assertEqual('#/definitions/%s' % key,
                         dr_1_props['copied_field_with_description']['$ref'])

        key = people_it + '__id'
        people_rels_props = people_props['relations']['items']['properties']
        self.assertIn('$ref', people_rels_props['relation'])
        self.assertEqual('#/definitions/%s' % key,
                         people_rels_props['relation']['$ref'])
        self.assertIn(key, doc['definitions'])

    def notest_data_relation_extended_description(self):
        doc = self.swagger_doc
        item_title = self.domain['dr_resource_1']['item_title']
        lookup_field = self.domain['dr_resource_1']['item_lookup_field']
        par = doc['parameters'][item_title+'_'+lookup_field]
        people_it = self.domain['people']['item_title']

        self.assertIn('description', par)
        self.assertEqual(
            'foobar copied_field (links to {0}_job)'.format(people_it),
            par['description'])

    def notest_data_relation_copied_description(self):
        doc = self.swagger_doc
        item_title = self.domain['dr_resource_2']['item_title']
        lookup_field = self.domain['dr_resource_2']['item_lookup_field']
        par = doc['parameters'][item_title+'_'+lookup_field]
        people_it = self.domain['people']['item_title']

        self.assertIn('description', par)
        self.assertEqual(
            'the job of the person (links to {0}_job)'.format(people_it),
            par['description'])

    def notest_header_parameters(self):
        doc = self.swagger_doc
        url = self.domain['people']['url']
        item_title = self.domain['people']['item_title']
        url = '/%s/{%sId}' % (url, item_title.lower())

        header_parameters = []
        # assume that header parameters are equal for PUT, PATCH, and DELETE
        for method in ['put', 'patch', 'delete']:
            for p in doc['paths'][url][method]['parameters']:
                if 'in' not in p:
                    continue
                if p['in'] == 'header':
                    if method in ['patch', 'delete']:
                        # already added in 'put'
                        self.assertIn(p, header_parameters)
                    else:
                        header_parameters += [p]

        self.assertTrue(len(header_parameters) == 1)
        h = header_parameters[0]
        self.assertIn('name', h)
        self.assertEqual(h['name'], 'If-Match')

    def notest_cors_without_origin(self):
        self.app.config['X_DOMAINS'] = ['http://example.com']
        self.app.config['X_HEADERS'] = ['Origin', 'X-Requested-With',
                                        'Content-Type', 'Accept']
        self.app.config['X_MAX_AGE'] = 2000
        r = self.test_client.get('/api-docs')

        self.assertEqual(r.status_code, 200)
        self.assertNotIn('Access-Control-Allow-Origin', r.headers)
        self.assertNotIn('Access-Control-Allow-Headers', r.headers)
        self.assertNotIn('Access-Control-Allow-Methods', r.headers)
        self.assertNotIn('Access-Control-Max-Age', r.headers)
        self.assertNotIn('Access-Control-Expose-Headers', r.headers)

    def notest_cors_with_origin(self):
        self.app.config['X_DOMAINS'] = 'http://example.com'
        self.app.config['X_HEADERS'] = ['Origin', 'X-Requested-With',
                                        'Content-Type', 'Accept']
        self.app.config['X_MAX_AGE'] = 2000
        r = self.test_client.get('/api-docs',
                                 headers={'Origin': 'http://example.com'})

        self.assertEqual(r.status_code, 200)
        self.assertIn('Access-Control-Allow-Origin', r.headers)
        self.assertEqual(r.headers['Access-Control-Allow-Origin'],
                         'http://example.com')
        self.assertIn('Access-Control-Allow-Headers', r.headers)
        self.assertEqual(
            set(r.headers['Access-Control-Allow-Headers'].split(', ')),
            set(['Origin', 'X-Requested-With', 'Content-Type', 'Accept']))
        self.assertIn('Access-Control-Allow-Methods', r.headers)
        self.assertEqual(
            set(r.headers['Access-Control-Allow-Methods'].split(', ')),
            set(['HEAD', 'OPTIONS', 'GET']))
        self.assertIn('Access-Control-Max-Age', r.headers)
        self.assertEqual(r.headers['Access-Control-Max-Age'],
                         '2000')

    def notest_tags(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']

        self.assertIn('tags', doc)
        tag_names = [tag['name'] for tag in doc['tags']]
        self.assertTrue(len([n for n in tag_names if n == item_title]) == 1)

        url = '/' + self.domain['people']['url']
        for m in ['get', 'post', 'delete']:
            path_m = doc['paths'][url][m]
            self.assertIn('tags', path_m)
            self.assertIn(item_title, path_m['tags'])

        url = '/%s/{%sId}' % (self.domain['people']['url'], item_title.lower())
        for m in ['get', 'patch', 'put', 'delete']:
            path_m = doc['paths'][url][m]
            self.assertIn('tags', path_m)
            self.assertIn(item_title, path_m['tags'])


if __name__ == '__main__':
    unittest.main()
