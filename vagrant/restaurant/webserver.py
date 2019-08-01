from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer 
import cgi  #common gateway interface

## import CRUD Operations from Lesson 1 ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Create session and connect DB

class webserverHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()				
				output = ""
				output += "<html><body>"
				output += "<h1>&#161Hola!</h1> <a href = '/hello' >Back to Hello</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output += "</body></html>"			
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()		
				#Create session and connect DB
				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind = engine)
				session = DBSession()
				#Query all Restaurants
				restaurants = session.query(Restaurant).all()
				output = ""
				output += "<html><body>"
				output += "<a href = '/restaurants/new' >Make a new restaurant here</a><br><br>"
				for restaurant in restaurants:
					output += restaurant.name
					output += "<br><a href = '/restaurants/%s/edit' >Edit</a>" % restaurant.id
					output += "<br><a href = '/restaurants/%s/delete' >Delete</a><br><br>" % restaurant.id
				output += "</body></html>"			
				self.wfile.write(output)
				print output
				#Close session and dispose engine
				session.close()
				engine.dispose()
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()		
				#Create session and connect DB
				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind = engine)
				session = DBSession()
				#Query all Restaurants
				items = session.query(Restaurant).all()
				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Make a new restaurant</h2><input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name' ><input type='submit' value='Create'> </form>"
				output += "</body></html>"	
				self.wfile.write(output)
				print output
				#Close session and dispose engine
				session.close()
				engine.dispose()
				return

			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]	
				print restaurantIDPath
				#Create session and connect DB
				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind = engine)
				session = DBSession()
				#Query all Restaurants
				restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if restaurant != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()	
					output = ""
					output += "<html><body>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><h2>%s</h2><input name='editedRestaurantName' type='text' placeholder = %s ><input type='submit' value='Rename'> </form>" %(restaurantIDPath, restaurant.name, restaurant.name)
					output += "</body></html>"	
					self.wfile.write(output)
					print output
				#Close session and dispose engine
				session.close()
				engine.dispose()
				return

			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]	
				print restaurantIDPath
				#Create session and connect DB
				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind = engine)
				session = DBSession()
				#Query all Restaurants
				restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if restaurant != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()	
					output = ""
					output += "<html><body>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><h1>Are you sure you want to delete %s?</h1><input type='submit' value='Delete'> </form>" %(restaurantIDPath, restaurant.name)
					output += "</body></html>"	
					self.wfile.write(output)
					print output
				#Close session and dispose engine
				session.close()
				engine.dispose()
				return
		
		except IOError:
			self.send_error(404, "File Not Found: %s" % self.path)

	def do_POST(self):
		try:

			if self.path.endswith("/restaurants/new"):				
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

				#Create session and connect DB
				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind = engine)
				session = DBSession()


				#Create new restaurant, add and commit to DB
				newRestaurant = Restaurant(name = messagecontent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

				#Close session and dispose engine
				session.close()
				engine.dispose()
				return

			if self.path.endswith("/edit"):		
				restaurantIDPath = self.path.split("/")[2]			
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('editedRestaurantName')

				#Create session and connect DB
				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind = engine)
				session = DBSession()


				#Create new restaurant, add and commit to DB
				restaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
				if restaurant != []:
					restaurant.name = messagecontent[0]
					session.add(restaurant)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

				#Close session and dispose engine
				session.close()
				engine.dispose()
				return

			if self.path.endswith("/delete"):		
				restaurantIDPath = self.path.split("/")[2]			
				
				#Create session and connect DB
				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind = engine)
				session = DBSession()


				#Create new restaurant, add and commit to DB
				restaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
				if restaurant != []:
					session.delete(restaurant)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

				#Close session and dispose engine
				session.close()
				engine.dispose()
				return

			#
			if self.path.endswith("/hello"):			
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output = ""
				output += "<html><body>"
				output += " <h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]

				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output +="</body></html>"
				self.wfile.write(output)
				print output
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()


	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()


if __name__ == '__main__':
	main()