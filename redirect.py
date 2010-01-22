import os
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class RedirectEntry(db.Model):
    owner = db.UserProperty()
    alias = db.StringProperty()
    redirect_to = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class Redirect(webapp.RequestHandler):
    def get(self):
        alias = self.request.path[3:] #omit leading '/r/'
        
        entry = RedirectEntry.all().filter('alias = ', alias).get()
        if entry is not None:
            self.redirect(entry.redirect_to)

        #return interface to make a redirect
        params = {}
        params['alias'] = alias

        path = os.path.join(os.path.dirname(__file__), 'MakeRedirect.html')
        self.response.out.write(template.render(path, params))
        
    def post(self):
        entry = RedirectEntry()
        entry.redirect_to = self.request.get('redirect_to')
        entry.alias = self.request.get('alias')
        if users.get_current_user():
            entry.owner = users.get_current_user()
        entry.put()
        self.redirect('/r/' + entry.alias)

application = webapp.WSGIApplication(
    [('/r/.*', Redirect)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()