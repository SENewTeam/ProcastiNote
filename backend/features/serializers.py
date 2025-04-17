from rest_framework import serializers
from features.models import ConferencesCache

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferencesCache
        fields = ('conference_id', 'conference_name', 'deadline', 'venue', 'conference_link')
