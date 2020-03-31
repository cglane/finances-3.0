from django.core.management.base import BaseCommand, CommandError
from transactions.import_helpers import upload_csv

class Command(BaseCommand):
	def handle(self, *args, **options):
		print('hello world')
		upload_csv("/Users/charleslane/Desktop/finances_django_app/import_csv.csv")