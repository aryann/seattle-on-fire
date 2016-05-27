import datetime
import json
import webapp2

from google.appengine.ext import ndb

import config
import models


class GetIncidentsHandler(webapp2.RequestHandler):

    def parse_time(self, time_string):
        return datetime.datetime.strptime(
            time_string, '%Y%m%d%H%M')

    def get(self):
        start = self.parse_time(self.request.get('start'))
        limit = self.parse_time(self.request.get('limit'))
        incidents = []
        for incident in models.Incident.query(
            ndb.AND(models.Incident.time >= start,
                    models.Incident.time < limit)):
            num_units = len(incident.units)
            incidents.append((incident.address, num_units))

        self.response.headers['Content-Type'] = 'text/json'
        self.response.write(json.dumps(incidents, indent=2))


handlers = webapp2.WSGIApplication([
    ('/fe/getincidents', GetIncidentsHandler),
], debug=config.DEBUG)
