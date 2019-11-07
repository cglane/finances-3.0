from rest_framework import serializers
from django.db import models
from django.contrib.auth.models import User
from transactions.models import Transaction

class TransactionSerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    location = serializers.CharField(max_length=30)
    amount = serializers.FloatField()
    description = serializers.CharField(max_length=30)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = ('date', 'location', 'amount', 'description')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Transaction.objects.create(**validated_data)

