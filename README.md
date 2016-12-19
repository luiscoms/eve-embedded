Eve-Embedded
===========

[![Build Status](https://travis-ci.org/ateliedocodigo/python-module-boilerplate.svg?branch=master)](https://travis-ci.org/ateliedocodigo/python-module-boilerplate)
[![Requirements Status](https://requires.io/github/ateliedocodigo/python-module-boilerplate/requirements.svg?branch=master)](https://requires.io/github/ateliedocodigo/python-module-boilerplate/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/ateliedocodigo/python-module-boilerplate/badge.svg?branch=master)](https://coveralls.io/github/ateliedocodigo/python-module-boilerplate?branch=master)

This project servers as an example of a Python package with some boilerplate
code already in place.


Usage
----

In the schema set the url

```python
schema = {
    "firstname": {
        "type": "string",
        "minlength": 1,
        "maxlength": 10,
    },
    "country": {
        "type": "string",
        "schema": {
            "type": "string",
            "data_relation": {
                "api": "http://api.example.com/country",
                "embeddable": True
            }
        }
    }
}
```

Then install the module

```python
from eve_emdedded import embedded

app = Eve()
embedded.install(app)
```


Running tests with `tox`
----

Install `tox`
```
$ pip install tox
```

Run tests

```
tox
```
