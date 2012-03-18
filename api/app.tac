from twisted.web import server
from twisted.application import service, internet

import api


application = service.Application("Hacker Trade API Webservice")
site = server.Site(api.API())
service = internet.TCPServer(6000, site)
service.setServiceParent(application)

