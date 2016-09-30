import datetime
import httplib
import json
import webapp2

from google.appengine.ext import ndb

import coordinate_utils
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
                    models.Incident.time < limit)).fetch(
                        config.MAX_INCIDENTS_TO_FETCH + 1):

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

        # TODO: Make this cooler by creating a separate handler for
        # getting the incidents, and using JavaScript to
        # asynchronously pull the data.
        incidents = self.get_incidents(start, limit)

        if len(incidents) > config.MAX_INCIDENTS_TO_FETCH:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(
                "Sorry, but I can't display more than {0} incidents at a time. "
                "Please choose a smaller time range.".format(config.MAX_INCIDENTS_TO_FETCH))
            self.response.set_status(httplib.BAD_REQUEST)
            return

        template = config.JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({
            'start': start.isoformat('T'),
            'limit': limit.isoformat('T'),
            'incidents': json.dumps(incidents, indent=2),
            'maps_api_key': config.MAPS_API_KEY,
        }))


class CanvasHandler(webapp2.RequestHandler):

    def get(self):
        data = [255] * (coordinate_utils.CANVAS_WIDTH *
                        coordinate_utils.CANVAS_HEIGHT)

        for incident in models.Incident.query(
                models.Incident.location != None).fetch(
                    10000):
            x, y = coordinate_utils.get_relative_placement(incident.location)

            # Out of bounds? Just skip!
            if not (0 <= x < coordinate_utils.CANVAS_WIDTH and
                    0 <= y < coordinate_utils.CANVAS_HEIGHT):
                continue

            data[y * coordinate_utils.CANVAS_WIDTH + x] = 0

        with open('seattle_outline.json') as f:
            seattle_outline = f.read().strip()

        template = config.JINJA_ENVIRONMENT.get_template('canvas.html')
        self.response.write(template.render({
            'height': coordinate_utils.CANVAS_HEIGHT,
            'width': coordinate_utils.CANVAS_WIDTH,
            'data': json.dumps(data),
            'seattleOutline': seattle_outline,
        }))


handlers = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/canvas', CanvasHandler),
], debug=config.DEBUG)
