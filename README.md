Eve-Embedded
===========

[![Build Status](https://travis-ci.org/luiscoms/eve-embedded.svg?branch=master)](https://travis-ci.org/luiscoms/eve-embedded)
[![Requirements Status](https://requires.io/github/luiscoms/eve-embedded/requirements.svg?branch=master)](https://requires.io/github/luiscoms/eve-embedded/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/luiscoms/eve-embedded/badge.svg?branch=master)](https://coveralls.io/github/luiscoms/eve-embedded?branch=master)

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
from eve_embedded import embedded

app = Eve()
embedded.install(app)
```


Running tests with `tox`
----

You will need an instance of `mongo` running locally

Install `tox`
```
$ pip install tox
```

Run tests

```
tox
```
