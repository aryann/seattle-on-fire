import os

import jinja2


DEBUG = True

MAPS_API_KEY = 'AIzaSyDJoU2NmXwoyMUCpZghJMyy_Q4Hi-WwGLU'

GEOCODING_API_KEY = 'AIzaSyCV-AkLrg985WgXnOmIx7uDhXOnPNXwtVA'

# How many incidents should be geocoded per cron request?
#
# The Geocoding API has a free tier that allows 2,500 requests per
# day. The geocoding handler is configured in cron.yaml to run once
# every two minutes. To stay under the limit, we aim for three
# requests per invocation of the handler, leading to 2,160 requests
# per day.
GEOCODING_BATCH_SIZE = 3

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=[
        'jinja2.ext.autoescape',
    ],
    autoescape=True)

MAX_INCIDENTS_TO_FETCH = 500

TOP_LEFT_SEATTLE_COORDS = (47.742476, -122.450239)
R_EARTH_METERS = 6371008.8
