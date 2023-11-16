from rest_framework import serializers
from .models import Connection

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'user1', 'user2', 'status', 'established_at']