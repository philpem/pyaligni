import Aligni

if __name__ == '__main__':
	a = Aligni.API('demo', 'oid3vLgynoy_Yl1gZkrgkLEq3J')

	print a.get_contact()
	print a.get_contact(4)
