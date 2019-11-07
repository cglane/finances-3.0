from django.test import TestCase
from transactions.models import Transaction
from django.contrib.auth.models import User
from transactions.import_helpers import upload_csv
class AnimalTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='12345')
		upload_csv("./test_csv.csv")

	def test_animals_can_speak(self):
		"""Animals that can speak are correctly identified"""
		transaction = Transaction.objects.get(amount='-46.42')
		assert transaction.source == 'Salary'