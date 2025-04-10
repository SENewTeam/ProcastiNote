from rest_framework import serializers
from .models import PaperInfo

class PaperInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperInfo
        fields = '__all__'

    paperPdf = serializers.CharField(required=False, allow_blank=True)
    venue = serializers.CharField(required=False, allow_blank=True)
    venue_link = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        # If 'paperPdf', 'venue', or 'venue_link' are not provided, set them to their default values
        validated_data.setdefault('paperPdf', "default_paper_pdf_url")
        validated_data.setdefault('venue', "default_venue")
        validated_data.setdefault('venue_link', "default_venue_link")

        # Call the default create method with the modified validated_data
        return super().create(validated_data)
