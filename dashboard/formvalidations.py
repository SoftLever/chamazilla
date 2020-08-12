import re

def phoneValidation(phone_number):
	if re.match('^07[0-9]{8}$', phone_number):
		return True
	else:
		return False