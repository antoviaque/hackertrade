# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Xavier Antoviaque <xavier@antoviaque.org>
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#

# Imports ##########################################################

import cgi, codecs
from pymongo.connection import Connection
from django.utils.html import urlize

# Func

def text2html(text):
    #text = to_unicode(text).decode("utf-8", "replace")
    text = unicode(text)
    text = cgi.escape(text)
    text = urlize(text, None)
    text = text.replace(u'\n', u'\n<br />') 
    return text


# Main #############################################################

f = codecs.open('applications/static/applications.html', 'w+', 'utf-8')

connection = Connection("localhost")
db = connection.hackertrade

with open('static/header.html') as fhead:
    f.write(fhead.read())

f.write(u'<div class="content">')
f.write(u'<hr /><h1>CLIENTS</h1><hr />')

for application in db.applications_clients.find({}):
    f.write(u'<h1>' + text2html(application['name']) + u' (' + text2html(application['company']) + u')</h1>')
    f.write(u'<ul>')
    f.write(u'<li><strong>Email:</strong> <a href="mailto:' + cgi.escape(application['email']) + u'">' + text2html(application['email']) + u'</a>')
    f.write(u'         (added: ' + application['date_added'].strftime("%Y-%m-%d %H:%M:%S") + u')</li>')
    f.write(u'<li><strong>Links:</strong> ' + text2html(application['links']) + u'</li>')
    f.write(u'<li><strong>Previous works:</strong> ' + text2html(application['previous_works']) + u'</li>')
    f.write(u'<li><strong>Project:</strong> ' + text2html(application['project']) + u'</li>')
    f.write(u'<li><strong>Test task:</strong> ' + text2html(application['test_task']) + u'</li>')
    f.write(u'</ul>')
    f.write(u'<p>&nbsp;</p><hr />')
    
f.write('<h1>HACKERS</h1><hr />')

for application in db.applications_hackers.find({}):
    f.write(u'<h1>' + text2html(application['name']) + u'</h1>')
    f.write(u'<ul>')
    f.write(u'<li><strong>Email:</strong> <a href="mailto:' + application['email'] + u'">' + text2html(application['email']) + u'</a>')
    f.write(u'         (added: ' + application['date_added'].strftime("%Y-%m-%d %H:%M:%S") + u'"</li>')
    f.write(u'<li><strong>Links:</strong> ' + text2html(application['links']) + u'</li>')
    f.write(u'<li><strong>Previous works:</strong> ' + text2html(application['previous_works']) + u'</li>')
    f.write(u'<li><strong>Price:</strong> ' + text2html(application['price']) + u'</li>')
    f.write(u'<li><strong>Availabilities:</strong> ' + text2html(application['availabilities']) + u'</li>')
    f.write(u'</ul>')
    f.write(u'<p>&nbsp;</p><hr />')

f.write(u'</div>')
with open('static/footer.html') as fhead:
    f.write(fhead.read())
    
f.close()
