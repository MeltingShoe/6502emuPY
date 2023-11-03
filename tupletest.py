class eval:
	def doIT(self):
		print('it did it')
e = eval()


print('boutta call')
toop = (True,e.doIT)
if(toop[0]):
	toop[1]()