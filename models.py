from google.appengine.ext import ndb


class Incident(ndb.Model):
    location = ndb.GeoPtProperty()
    address = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(required=True)
    units = ndb.StringProperty(repeated=True)
    original_text = ndb.TextProperty(repeated=True)
