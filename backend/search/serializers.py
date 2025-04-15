from rest_framework import serializers

from search.models import History

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['details', 'created_at']