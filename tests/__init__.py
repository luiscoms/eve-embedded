import json
import os
import unittest

import eve
from bson import ObjectId
from flask_pymongo import MongoClient

import eve_embedded.embedded
from tests.test_settings import \
    MONGO_HOST, MONGO_PORT, \
    MONGO_USERNAME, MONGO_PASSWORD, MONGO_DBNAME


class TestBase(unittest.TestCase):

    test_data = {
        "skills": [
            {
                '_id': ObjectId('570c24f8de9f0c5e6c7a2e71'),
                'name': "Programming"
            },
            {
                '_id': ObjectId('570c24fbde9f0c5e6c7a2e9f'),
                'name': "Reading"
            },
        ],
        "people": [
            {
                '_id': ObjectId('54f112defba522406c9cc209'),
                'name': "John",
                "skills": [ObjectId('570c24f8de9f0c5e6c7a2e71'), ObjectId('570c24fbde9f0c5e6c7a2e9f')]
            },
            {
                '_id': ObjectId('585a8be8f0983235bf0f95ed'),
                'name': "Peter",
                "rest_skills": ['570c24f8de9f0c5e6c7a2e71', '570c24fbde9f0c5e6c7a2e9f']
            }
        ]
    }

    def setUp(self, settings=None):
        self.this_directory = os.path.dirname(os.path.realpath(__file__))
        if settings is None:
            settings = os.path.join(self.this_directory, 'test_settings.py')

        self.setupDB()

        self.settings = settings
        self.app = eve.Eve(settings=self.settings)
        eve_embedded.embedded.install(self.app)

        self.test_client = self.app.test_client()
        self.domain = self.app.config['DOMAIN']

    def tearDown(self):
        del self.app
        self.dropDB()

    def setupDB(self):
        self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
        self.connection.drop_database(MONGO_DBNAME)
        if MONGO_USERNAME:
            self.connection[MONGO_DBNAME].add_user(MONGO_USERNAME,
                                                   MONGO_PASSWORD)

        # seed
        self.connection[MONGO_DBNAME] \
            .skills \
            .insert_many(self.test_data.get("skills"))
        self.connection[MONGO_DBNAME] \
            .people \
            .insert_many(self.test_data.get("people"))

    def dropDB(self):
        self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
        self.connection.drop_database(MONGO_DBNAME)
        self.connection.close()

    def parse_response(self, r):
        try:
            v = json.loads(r.get_data().decode('utf-8'))
        except ValueError:
            v = None
        return v
