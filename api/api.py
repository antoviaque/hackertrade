

# Imports ##########################################################

import txmongo
from datetime import datetime

from twisted.internet import defer
from twisted.web import resource, server, error


# Config ###########################################################

DOMAIN = "http://hackertrade.com"


# Functions ########################################################

@defer.inlineCallbacks
def get_db():
    mongo = yield txmongo.MongoConnection()
    db = mongo.hackertrade
    defer.returnValue(db)

def notify_team(subject, text):
    import smtplib
    import string
 
    body = string.join((
            "From: Hacker Trade Applications <team@hackertrade.com>",
            "To: team@hackertrade.com",
            "Subject: %s" % subject,
            "",
            text
            ), "\r\n")
    server = smtplib.SMTP('localhost')
    server.sendmail('team@hackertrade.com', ['team@hackertrade.com'], body)
    server.quit()


# Classes ##########################################################

class API(resource.Resource):
    def getChild(self, name, request):
        if name == 'api':
            return self
        elif name == 'application':
            return Application()
        else:
            return error.NoResource()

class Application(resource.Resource):        
    isLeaf = True
    
    def render_POST(self, request):
        if request.postpath != ['client'] and request.postpath != ['hacker']:
            request.setResponseCode(400)
            return "<html><body>Wrong application type.</body></html>"
        role = request.postpath[0]
        
        d = self.record_application(role, request.args)
        d.addCallback(self.respond, request)
        return server.NOT_DONE_YET
        
    @defer.inlineCallbacks
    def record_application(self, role, args):
        db = yield get_db()
        if role == 'client':
            applications = db.applications_clients
            fields_names = ['project', 'name', 'links', 'test_task', 'company', 'email', 'previous_works']
        elif role == 'hacker':
            applications = db.applications_hackers
            fields_names = ['availabilities', 'name', 'links', 'price', 'email', 'previous_works']
                
        new_application = {}
        new_application['date_added'] = datetime.now()
        for field_name in fields_names:
            if field_name in args:
                new_application[field_name] = args[field_name][0]
        
        result = yield applications.insert(new_application, safe=True)

        if role == 'client':
            notify_team("New client application!", repr(new_application))

        defer.returnValue(result)

    def respond(self, result, request):
        if result:
            request.setHeader("Refresh", "0; url=%s/apply_success.html" % DOMAIN)
        else:
            request.setHeader("Refresh", "0; url=%s/apply_error.html" % DOMAIN)
            
        request.finish()
        
