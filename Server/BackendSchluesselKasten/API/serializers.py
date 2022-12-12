from rest_framework import serializers
from .models import Tour, Account
from django.utils import timezone


class TourSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tour
        exclude = ['owner', 'mutable']

    def create(self, validated_data):
        return Tour.objects.create(owner=Account.objects.get(uid=self.context['uid']), **validated_data)

    def update(self, instance, validated_data):
        instance.back = True
        instance.end = timezone.now()
        instance.save()
        return instance
