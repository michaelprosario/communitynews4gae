import os
import urllib
import cgi
import datetime
import time
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb




JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'])
SLEEP_FACTOR = 2

import webapp2

#================================================================================

class CommunityPosts(ndb.Model):    
	createdBy = ndb.StringProperty()
	createdAt = ndb.DateTimeProperty()
	updatedBy = ndb.StringProperty()
	updatedAt = ndb.DateTimeProperty()
	content = ndb.StringProperty()

#===============================================================================
	
def loadFrontPage(self):
	user = users.get_current_user()

	if user:
		posts = CommunityPosts().query().order(-CommunityPosts.createdAt).fetch()
		data = {"posts":posts, "user": user.email(), "logout_url":  users.create_logout_url(self.request.uri) }
		template = JINJA_ENVIRONMENT.get_template('list_posts.html')
		self.response.write(template.render(data))	
	else:
		self.redirect(users.create_login_url(self.request.uri))

#===============================================================================
	
class MainHandler(webapp2.RequestHandler):
	def get(self):
		loadFrontPage(self)

#===============================================================================
        
class PostHandler(webapp2.RequestHandler):
    def post(self):        		
		postInput = cgi.escape(self.request.get('postInput'))
		
		user = users.get_current_user()
		
		aPost = CommunityPosts()
		aPost.createdBy = user.email()
		aPost.updatedBy = user.email()
		aPost.createdAt = datetime.datetime.now()
		aPost.updatedAt = datetime.datetime.now()
		aPost.content = postInput
		aPost.put()
		
		time.sleep(SLEEP_FACTOR)
		self.redirect("/")

#===============================================================================
		
class DeletePostHandler(webapp2.RequestHandler):
    def get(self):        		
		id = cgi.escape(self.request.get('id'))
		id = int(id)
		aPost = CommunityPosts().get_by_id(id)
		aPost.key.delete()		
		time.sleep(SLEEP_FACTOR)		
		self.redirect("/")

#===============================================================================

app = webapp2.WSGIApplication([
    ('/',           MainHandler), 
	('/handlePost', PostHandler),
	('/deletePost', DeletePostHandler)
], debug=True)
