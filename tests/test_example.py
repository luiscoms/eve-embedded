import json
import unittest
from pprint import pprint

import httpretty

from tests import TestBase  # noqa: E402


class TestEveEmbedded(TestBase):

    @httpretty.activate
    def test_embedded_rest_relation(self):
        httpretty.disable()

        peter_skills = '/people/585a8be8f0983235bf0f95ed'
        people = self.parse_response(self.test_client.get(peter_skills))
        expected = people.copy()
        # swap skills
        # expected["skills"], expected["rest_skills"] = expected["rest_skills"], expected["skills"]
        peter_rest_skills = '/people/585a8be8f0983235bf0f95ed?embedded={"rest_skills":1}'

        expected["rest_skills"] = []
        httpretty.enable()
        skill = self.parse_response(self.test_client.get('/skills/570c24f8de9f0c5e6c7a2e71'))
        skill.pop("_links", None)
        httpretty.register_uri(httpretty.GET,
                               'http://localhost:8080/skills/570c24f8de9f0c5e6c7a2e71',
                               content_type="application/json",
                               body=json.dumps(skill))
        expected["rest_skills"].append(skill)
        skill = self.parse_response(self.test_client.get('/skills/570c24fbde9f0c5e6c7a2e9f'))
        skill.pop("_links", None)
        httpretty.register_uri(httpretty.GET,
                               'http://localhost:8080/skills/570c24fbde9f0c5e6c7a2e9f',
                               content_type="application/json",
                               body=json.dumps(skill))
        expected["rest_skills"].append(skill)

        people = self.parse_response(self.test_client.get(peter_rest_skills))
        self.assertEqual(expected, people)

    @unittest.skip
    # def notest_doc_is_dict(self):
    def test_embedded_relations(self):
        doc = self.test_client \
            .get('/people?embedded={"relations.relation":1}') \
            .get_data() \
            .decode('utf-8')

        # self.assertEqual(doc.status_code, 200)

        j = json.loads(doc)
        print("--ls--" * 10)
        pprint(j)
        self.assertIn('_items', doc)
        # self.assertIsInstance(doc, dict)

    @httpretty.activate
    @unittest.skip
    def test_embedded_rest_relations(self):
        httpretty.disable()

        expected = self.test_client \
            .get('/people') \
            .get_data() \
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
        print("register http://myapi.com/people/54f112defba522406c9cc209",
              type(json.dumps(expected_json.get('_items')[0])))
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


if __name__ == '__main__':
    unittest.main()
