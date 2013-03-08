import Aligni

if __name__ == '__main__':
	a = Aligni.API('demo', 'oid3vLgynoy_Yl1gZkrgkLEq3J')

	m = a.get_manufacturer()
	print a.get_manufacturer(m[0].id)
	print

	v = a.get_vendor()
	print a.get_vendor(v[0].id)
	print

	c = a.get_contact()
	print a.get_contact(c[0].id)
	print

	pt = a.get_parttype()
	print a.get_parttype(pt[0].id)
	print

	p = a.get_part()
	print a.get_part(p[0].id)
	print

	units = dict()
	for u in a.get_unit():
		unit = a.get_unit(u.id)
		units[u.id] = unit
		print unit
	print
