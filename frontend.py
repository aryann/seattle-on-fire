import datetime
import json
import webapp2

from google.appengine.ext import ndb

import config
import models


class MainHandler(webapp2.RequestHandler):

    def parse_rfc3339_time(self, time_string):
        return datetime.datetime.strptime(
            time_string, '%Y-%m-%dT%H:%M:%S.%f')

    def get_incidents(self, start, limit):
        incidents = []
        for incident in models.Incident.query(
            ndb.AND(models.Incident.time >= start,
                    models.Incident.time < limit)):

            # Has the address been geocoded yet? If not, skip the
            # record.
            if not incident.location:
                continue

            num_units = len(incident.units)
            incidents.append((
                    (incident.location.lat, incident.location.lon),
                    num_units))
        return incidents

    def get(self):
        start = self.request.get('start')
        limit = self.request.get('limit')
        if start and limit:
            start = self.parse_rfc3339_time(start)
            limit = self.parse_rfc3339_time(limit)
        elif start or limit:
            self.redirect('/')
            return
        else:
            # Gets the current time in PST. Note that this does not handle
            # daylight savings! It's too much work and too tricky to
            # support daylight savings, so I have favored a simple method
            # that ignores daylight savings. :)
            limit = datetime.datetime.utcnow() - datetime.timedelta(hours=7)
            start = limit - datetime.timedelta(days=1)

        now_pst = datetime.datetime.utcnow() - datetime.timedelta(hours=7)

        incidents = self.get_incidents(start, limit)

        template = config.JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({
            'start': start.isoformat('T'),
            'limit': limit.isoformat('T'),
            'incidents': json.dumps(incidents, indent=2),
            'maps_api_key': config.MAPS_API_KEY,
        }))


handlers = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=config.DEBUG)
