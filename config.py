import os

import jinja2


DEBUG = True

MAPS_API_KEY = 'AIzaSyDJoU2NmXwoyMUCpZghJMyy_Q4Hi-WwGLU'

GEOCODING_API_KEY = 'AIzaSyCV-AkLrg985WgXnOmIx7uDhXOnPNXwtVA'

# How many incidents should be geocoded per cron request?
GEOCODING_BATCH_SIZE = 10

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=[
        'jinja2.ext.autoescape',
    ],
    autoescape=True)
