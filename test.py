import Aligni

if __name__ == '__main__':
	a = Aligni.API('demo', 'oid3vLgynoy_Yl1gZkrgkLEq3J')

	m = a.get_manufacturer()
	print a.get_manufacturer(m[0].id)

	v = a.get_vendor()
	print a.get_vendor(v[0].id)

	c = a.get_contact()
	print a.get_contact(c[0].id)
