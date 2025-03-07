from rest_framework import serializers
from .models import Inventory, Member, Booking


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'surname', 'booking_count', 'date_joined']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'title', 'description', 'remaining_count', 'expiration_date']


class BookingSerializer(serializers.ModelSerializer):
    member_details = MemberSerializer(source='member', read_only=True)
    item_details = InventorySerializer(source='title', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'member',
            'title',
            'booking_date',
            'member_details',
            'item_details'
        ]
        read_only_fields = ['booking_date']

