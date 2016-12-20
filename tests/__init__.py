import os
import json

import eve
import eve_embedded.embedded
from flask_pymongo import MongoClient
from tests.test_settings import \
    MONGO_HOST, MONGO_PORT, \
    MONGO_USERNAME, MONGO_PASSWORD, MONGO_DBNAME

import unittest


class TestBase(unittest.TestCase):
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
        result = self.connection[MONGO_DBNAME].people.\
            insert_one({
                'name': "John"
            })
        result = self.connection[MONGO_DBNAME].people.\
            insert_one({
                'name': "Peter",
                "relations": [
                    {
                        "relation_type": "family",
                        "relation": result.inserted_id,
                    }
                ],
                "rest_relations": [
                    {
                        "relation_type": "family",
                        "relation": result.inserted_id,
                    }
                ]
            })
        # result = self.connection[MONGO_DBNAME].people.\
        #     insert_one({'name': "Peter"})

        # print(result.inserted_id)
        # ObjectId('54f112defba522406c9cc208')

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
