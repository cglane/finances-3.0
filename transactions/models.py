from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
	date = models.DateField()
	location = models.CharField(max_length=150)
	amount = models.FloatField()
	description = models.CharField(max_length=100)
	source = models.CharField(max_length=100)
	notes = models.TextField()
	user = models.ForeignKey(User, unique=False, default=1, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'transactions'

	def __str__(self):  # __unicode__ on Python 2
		return self.location + ' - ' + str(self.date)

