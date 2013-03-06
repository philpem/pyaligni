import os, requests
import xml.etree.ElementTree as ET

# from http://www.devx.com/opensource/Article/33153
def __pretty_dump(e, ind=''):
	# start with indentation
	s = ind
	# put tag (don't close it just yet)
	s += '<' + e.tag
	# add all attributes
	for (name, value) in e.items():
		s += ' ' + name + '=' + "'%s'" % value
	# if there is text close start tag, add the text and add an end tag
	if e.text and e.text.strip():
		s += '>' + e.text + '</' + e.tag + '>'
	else:
		# if there are children...
		if len(e) > 0:
			# close start tag
			s += '>'
			# add every child in its own line indented
			for child in e:
				s += os.linesep + __pretty_dump(child, ind + '  ')
			# add closing tag in a new line
			s += os.linesep + ind + '</' + e.tag + '>'
		else:
			# no text and no children, just close the starting tag
			s += ' />'
	return s

class Entity:
	def __init__(self):
		pass

	def __repr__(self):
		return str(self.__dict__)

class Manufacturer(Entity):
	pass

class Vendor(Entity):
	pass

class Contact(Entity):
	pass

class API:
	''' Aligni API handler for Python '''

	def __init__(self, sitename, apikey):
		self.sitename = sitename
		self.apikey = apikey
		self.session = requests.Session()
		self.session.headers.update({'Accept':'application/xml', 'Content-Type':'application/xml'})
		# TODO: make a simple API request to ensure the apikey is correct?

	def __requ(self, endpoint):
		r = self.session.get("http://%s.aligni.com/api/%s/%s" % (self.sitename, self.apikey, endpoint))
		return ET.fromstring(r.text)

	def get_contact(self, cid=None):
		'''
		Get a contact or list of contacts from the Aligni API

		When 'cid' is not specified, a list of contacts will be returned.
		Only the 'id', 'firstname', 'lastname' and 'email' fields will
		contain data.

		When 'cid' is specified, an single, complete contact record
		containing the full details of the contact will be returned.
		'''

		def __parse_contact(et):
			o = Contact()
			for attr in et:
				setattr(o, attr.tag, attr.text)
			return o


		if cid is None:
			resp = self.__requ('contact/')
		else:
			resp = self.__requ('contact/%d' % cid)

		# Parse the response
		rval = list()
		if resp.tag == 'contacts':
			# More than one contact returned
			for contactInfo in resp:
				rval.append(__parse_contact(contactInfo))
		else:
			# One contact returned
			rval.append(__parse_contact(resp))

		return rval

