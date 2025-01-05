# ipo_app/serializers.py
from rest_framework import serializers
from .models import IPO  # Assuming IPO is your model

class IPOSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPO  # Ensure that IPO is a model in your app
        fields = '__all__'  # Or specify the fields you want
