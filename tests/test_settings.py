MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'test_user'
MONGO_PASSWORD = 'test_pw'
MONGO_DBNAME = 'eve_embedded_test'

TRANSPARENT_SCHEMA_RULES = True
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {
    'roles': {
        'type': 'dict',
        'schema': {
            'title': {
                'type': 'string',
                'required': True,
                'unique': True,
            },
            'people': {
                'type': 'list',
                'schema': {
                    "type": "objectid",
                    "data_relation": {
                        "resource": "people",
                        "embeddable": True
                    }
                }
            },
            'rest_people': {
                'type': 'list',
                'schema': {
                    "type": "string",
                    "data_relation": {
                        "api": "http://localhost:8080/people",
                        "embeddable": True
                    }
                }
            },
        },
    },
    'people': {
        'description': 'the people resource',
        'type': 'dict',
        'schema': {
            'name': {
                'type': 'string',
                'required': True,
                'unique': True,
                'description': 'the last name of the person'
            },
            'skills': {
                'type': 'list',
                'schema': {
                    "type": "objectid",
                    "data_relation": {
                        "resource": "skills",
                        "embeddable": True
                    }
                }
            },
            'rest_skills': {
                'type': 'list',
                'schema': {
                    "type": "string",
                    "data_relation": {
                        "api": "http://localhost:8080/skills",
                        "embeddable": True
                    }
                }
            },
            # 'job': {
            #     'type': 'string',
            #     'schema': {
            #         'relation': {
            #             'type': 'objectid',
            #             'data_relation': {
            #                 'resource': 'people',
            #                 # 'field': '_id',
            #                 "embeddable": True,
            #             }
            #         }
            #     }
            # },
            'relations': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'relation_type': {
                            'type': 'string',
                            'required': True
                        },
                        'relation': {
                            'type': 'objectid',
                            'data_relation': {
                                'resource': 'people',
                                'field': '_id',
                                "embeddable": True,
                            }
                        }
                    }
                }
            },
            'rest_relations': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'relation_type': {
                            'type': 'string',
                            'required': True
                        },
                        'relation': {
                            'type': 'string',
                            'data_relation': {
                                "api": 'http://localhost:8080/people',
                                # "api": 'http://myapi.com/people',
                                "embeddable": True,
                            }
                        }
                    }
                }
            }
        }
    },
    'skills': {
        'type': 'dict',
        'schema': {
            'name': {
                'type': 'string',
                'required': True,
                'unique': True,
            },
        },
    },
    'dr_resource_1': {
        'type': 'dict',
        'item_lookup_field': 'copied_field_with_description',
        'schema': {
            'copied_field_with_description': {
                'type': 'string',
                'description': 'foobar copied_field',
                'data_relation': {
                    'resource': 'people',
                    'field': 'job'
                }
            },
        }
    },
    'dr_resource_2': {
        'type': 'dict',
        'item_lookup_field': 'copied_field_without_description',
        'schema': {
            'copied_field_without_description': {
                'type': 'string',
                'data_relation': {
                    'resource': 'people',
                    'field': 'job'
                }
            }
        }
    }
}
