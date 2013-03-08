import os, requests
import xml.etree.ElementTree as ET

# from http://www.devx.com/opensource/Article/33153
def _pretty_dump(e, ind=''):
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
				s += os.linesep + _pretty_dump(child, ind + '  ')
			# add closing tag in a new line
			s += os.linesep + ind + '</' + e.tag + '>'
		else:
			# no text and no children, just close the starting tag
			s += ' />'
	return s

class Entity:
	int_params = ['id']

	def __init__(self, et):
		'''
		Initialise a default Entity from an ElementTree
		'''
		for attr in et:
			if attr.tag in self.int_params:
				setattr(self, attr.tag, int(attr.text))
			else:
				setattr(self, attr.tag, attr.text)

	def __repr__(self):
		return str(self.__dict__)

class Manufacturer(Entity):
	def __init__(self, et):
		'''
		Initialise a Manufacturer from an ElementTree
		'''
		for attr in et:
			if attr.tag == 'vendors':
				self.vendors = []
				for v in attr:
					self.vendors.append(Vendor(v))
			elif attr.tag in self.int_params:
				setattr(self, attr.tag, int(attr.text))
			else:
				setattr(self, attr.tag, attr.text)


class Vendor(Entity):
	def __init__(self, et):
		'''
		Initialise a Vendor from an ElementTree
		'''
		for attr in et:
			if attr.tag == 'manufacturers':
				self.manufacturers = []
				for m in attr:
					self.manufacturers.append(Manufacturer(m))
			elif attr.tag in self.int_params:
				setattr(self, attr.tag, int(attr.text))
			else:
				setattr(self, attr.tag, attr.text)


class Contact(Entity):
	int_params = ['id', 'vendor_id']


class PartType(Entity):
	pass


class AlternatePart(Entity):
	int_params = ['part_id', 'quality']


class VendorPartNumber(Entity):
	int_params = ['vendor_id']


class Quote(Entity):
	int_params = ['quantity_min', 'vendor_id', 'leadtime', 'quantity_mult', 'id']


class Part(Entity):
	int_params = ['id', 'parttype_id', 'manufacturer_id', 'rohs']

	def __init__(self, et):
		'''
		Initialise a Part from an ElementTree
		'''
		for attr in et:
			if attr.tag in self.int_params:
				setattr(self, attr.tag, int(attr.text))
			elif attr.tag == 'alternate_parts':
				self.alternate_parts = []
				for m in attr:
					self.alternate_parts.append(AlternatePart(m))
			elif attr.tag == 'quotes':
				self.quotes = []
				for m in attr:
					self.quotes.append(Quote(m))
			elif attr.tag == 'custom_parameters':
				self.custom_parameters = dict()
				for m in attr:
					self.custom_parameters[m.tag] = m.text
			elif attr.tag == 'vendor_part_numbers':
				self.vendor_part_numbers = []
				for m in attr:
					self.vendor_part_numbers.append(VendorPartNumber(m))
			else:
				setattr(self, attr.tag, attr.text)


class UnitConversion(Entity):
	int_params = ['id', 'to_unit_id']


class Unit(Entity):
	def __init__(self, et):
		'''
		Initialise a default Entity from an ElementTree
		'''
		for attr in et:
			if attr.tag in self.int_params:
				setattr(self, attr.tag, int(attr.text))
			elif attr.tag == 'unit_conversions':
				self.unit_conversions = []
				for m in attr:
					self.unit_conversions.append(UnitConversion(m))
			else:
				setattr(self, attr.tag, attr.text)


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
		with open("log","wt") as f:
			f.write(r.text)
		return ET.fromstring(r.text)


	def get_manufacturer(self, mid=None):
		'''
		Get a manufacturer or list of manufacturers from the Aligni API
		'''
		if mid is None:
			resp = self.__requ('manufacturer/')
		else:
			resp = self.__requ('manufacturer/%d' % mid)

		# Parse the response
		rval = list()
		if resp.tag == 'manufacturers':
			# More than one manufacturer returned
			for manufacturerInfo in resp:
				rval.append(Manufacturer(manufacturerInfo))
		else:
			# One manufacturer returned
			rval.append(Manufacturer(resp))

		return rval


	def get_vendor(self, mid=None):
		'''
		Get a vendor or list of vendors from the Aligni API
		'''
		if mid is None:
			resp = self.__requ('vendor/')
		else:
			resp = self.__requ('vendor/%d' % mid)

		# Parse the response
		rval = list()
		if resp.tag == 'vendors':
			# More than one vendor returned
			for vendorInfo in resp:
				rval.append(Vendor(vendorInfo))
		else:
			# One vendor returned
			rval.append(Vendor(resp))

		return rval


	def get_contact(self, cid=None):
		'''
		Get a contact or list of contacts from the Aligni API

		When 'cid' is not specified, a list of contacts will be returned.
		Only the 'id', 'firstname', 'lastname' and 'email' fields will
		contain data.

		When 'cid' is specified, an single, complete contact record
		containing the full details of the contact will be returned.
		'''
		if cid is None:
			resp = self.__requ('contact/')
		else:
			resp = self.__requ('contact/%d' % cid)

		# Parse the response
		rval = list()
		if resp.tag == 'contacts':
			# More than one contact returned
			for contactInfo in resp:
				rval.append(Contact(contactInfo))
		else:
			# One contact returned
			rval.append(Contact(resp))

		return rval


	def get_parttype(self, ptid=None):
		'''
		Get a parttype or list of parttypes from the Aligni API

		When 'ptid' is not specified, a list of parttypes will be returned.
		Only the 'id', 'firstname', 'lastname' and 'email' fields will
		contain data.

		When 'ptid' is specified, an single, complete parttype record
		containing the full details of the parttype will be returned.
		'''
		if ptid is None:
			resp = self.__requ('parttype/')
		else:
			resp = self.__requ('parttype/%d' % ptid)

		# Parse the response
		rval = list()
		if resp.tag == 'parttypes':
			# More than one parttype returned
			for parttypeInfo in resp:
				rval.append(PartType(parttypeInfo))
		else:
			# One parttype returned
			rval.append(PartType(resp))

		return rval


	def get_part(self, pid=None):
		'''
		Get a part or list of parts from the Aligni API

		When 'pid' is not specified, a list of parts will be returned.
		Only the 'id', 'firstname', 'lastname' and 'email' fields will
		contain data.

		When 'pid' is specified, an single, complete part record
		containing the full details of the part will be returned.
		'''
		if pid is None:
			resp = self.__requ('part/')
		else:
			resp = self.__requ('part/%d' % pid)

		# Parse the response
		rval = list()
		if resp.tag == 'parts':
			# More than one part returned
			for partInfo in resp:
				rval.append(Part(partInfo))
		else:
			# One part returned
			rval.append(Part(resp))

		return rval


	def get_unit(self, uid=None):
		'''
		Get a unit or list of units from the Aligni API

		When 'uid' is not specified, a list of units will be returned.
		Only the 'id', 'firstname', 'lastname' and 'email' fields will
		contain data.

		When 'uid' is specified, an single, complete unit record
		containing the full details of the unit will be returned.
		'''
		if uid is None:
			resp = self.__requ('unit/')
		else:
			resp = self.__requ('unit/%d' % uid)

		# Parse the response
		rval = list()
		if resp.tag == 'units':
			# More than one unit returned
			for unitInfo in resp:
				rval.append(Unit(unitInfo))
		else:
			# One unit returned
			rval.append(Unit(resp))

		return rval

