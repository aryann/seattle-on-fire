import datetime
import httplib
import json
import logging
import re
import urllib
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import config
import models


def extract_td_text(line):
    return re.search(r'<td.*">(.*)</td>', line).group(1)


class GetDataHandler(webapp2.RequestHandler):

    def get(self):
        # Yup, we are just using the Seattle's web UI for 911
        # calls. There is an API available for this
        # (https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj),
        # but it lacks timestamps, and it doesn't really have all the
        # data.
        url = ('http://www2.seattle.gov/fire/realtime911/getRecsForDatePub.asp?'
               'action=Today&incDate=&rad1=des')
        res = urlfetch.fetch(url)
        if res.status_code != httplib.OK:
            raise ValueError(
                'The request failed with error code {0}: {1}'.format(
                    res.status_code, res.content))

        lines = res.content.splitlines()
        bulk_insertions = []

        for i in xrange(len(lines)):
            if '<tr id=row_' not in lines[i]:
                continue

            time_string = extract_td_text(lines[i + 1])
            incident_id = extract_td_text(lines[i + 2])
            units = extract_td_text(lines[i + 4]).split()
            address = extract_td_text(lines[i + 5])
            type = extract_td_text(lines[i + 6])

            # TODO: Make this code more defensive, so we don't fail
            # due to one bad record.

            # TODO: This datetime object does not have any timezone
            # data. As of this writing, the offset is PDT. At some
            # point, this code should be amended to add timezone
            # information.
            time = datetime.datetime.strptime(
                time_string, '%m/%d/%Y %H:%M:%S %p')

            incident = models.Incident.get_by_id(incident_id)
            if incident:
                # Have more units been dispatched for the incident? If
                # so, update the number of units.
                for current_unit in units:
                    if current_unit not in incident.units:
                        incident.units = set(incident.units + units)
                        incident.put()
                        break
            else:
                bulk_insertions.append(models.Incident(
                        id=incident_id,
                        address=address,
                        units=units,
                        type=type,
                        time=time,
                        original_text=lines[i:i+8],
                ))

        if bulk_insertions:
            ndb.put_multi(bulk_insertions)


class GeocodeHandler(webapp2.RequestHandler):

    def get(self):
        for incident in models.Incident.query(
            models.Incident.location == None).order(
                -models.Incident.time).fetch(
                    config.GEOCODING_BATCH_SIZE):

            url = ('https://maps.googleapis.com/maps/api/geocode/'
                   'json?address={address}&key={key}').format(
                address=urllib.quote_plus(
                    incident.address + ', Seattle, WA, USA'),
                key=config.GEOCODING_API_KEY)
            logging.info('Geocoding request: %s', url)

            res = json.loads(urlfetch.fetch(url).content)
            location = res['results'][0]['geometry']['location']
            incident.location = ndb.GeoPt(lat=location['lat'], lon=location['lng'])
            incident.put()


handlers = webapp2.WSGIApplication([
    ('/admin/getdata', GetDataHandler),
    ('/admin/geocode', GeocodeHandler),
], debug=config.DEBUG)
