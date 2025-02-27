from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    qr_code = serializers.ImageField(read_only=True)  # Add QR code to API response

    class Meta:
        model = Item
        fields = '__all__'
