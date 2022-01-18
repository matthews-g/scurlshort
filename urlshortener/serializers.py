from rest_framework import serializers
from urlshortener.models import ShortUrlModel


class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortUrlModel
        fields = ['shortcode', 'url', 'creation_date', 'last_redirect', 'redirect_count']