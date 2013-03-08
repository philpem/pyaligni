import sys,os
import Aligni

if __name__ == '__main__':
	a = Aligni.API('demo', 'oid3vLgynoy_Yl1gZkrgkLEq3J')

	invlocs = dict()
	for il in a.get_inventory_location():
		invloc = a.get_inventory_location(il.id)
		# get sublocations too
		subl = invloc.inventory_sublocations
		invloc.inventory_sublocations = []
		for isl in subl:
			invloc.inventory_sublocations.append(a.get_inventory_sublocation(isl.id))
		invlocs[il.id] = invloc
		print invloc
	print

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
