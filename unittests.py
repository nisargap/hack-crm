import unittest

import datetime

from jsonschema import validate

def contact_schema(test_object):

	try:
		import jsonschema

		import schemas

		try:

			validate(test_object, schemas.contact)

			return True

		except ValidationError:

			return False


	except:

		return False


class contact_test_success(unittest.TestCase):

	def test(self):

		test_object = {
			"name" : "John",
			"company" : "Company",
			"datetime" : str(datetime.datetime.utcnow()),
			"email" : "john@email.com"
		}


		self.assertEqual(contact_schema(test_object), True)

class contact_test_fail(unittest.TestCase):

	def test(self):

		test_object = {
			"company" : "Company",
			"datetime" : str(datetime.datetime.utcnow()),
		}


		self.assertEqual(contact_schema(test_object), False)




