from django.core.management.base import BaseCommand, CommandError
from transactions.import_helpers import upload_csv

class Command(BaseCommand):
	def handle(self, *args, **options):
		upload_csv("/Users/charles/Downloads/finances-imports.csv")