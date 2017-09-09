# from tests import TestBase
from eve import Eve
from eve_embedded import embedded

application = Eve(import_name="app", settings='test_settings.py')
embedded.install(application)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)
