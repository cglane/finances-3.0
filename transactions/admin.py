from django.contrib import admin
from transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
	list_display = ('order_id_display', 'location', 'amount', 'date', 'description')

	def order_id_display(self, obj):
		return obj.user.id


admin.site.register(Transaction, TransactionAdmin)