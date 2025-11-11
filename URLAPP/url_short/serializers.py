from rest_framework import serializers
from .models import URL

class URLSerializer(serializers.ModelSerializer):
    custom_alias = serializers.CharField(required=False, allow_blank=True)
    expiration_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = URL
        fields = ['original_url', 'custom_alias', 'expiration_date']

    def create(self, validated_data):
        alias = validated_data.pop('custom_alias', None)
        expiration_date = validated_data.pop('expiration_date', None)

        if alias and URL.objects.filter(short_code=alias).exists():
            raise serializers.ValidationError({"custom_alias": "Alias already exists."})

        short_code = alias if alias else None
        url = URL.objects.create(
            original_url=validated_data['original_url'],
            short_code=short_code or None,
            expires_at=expiration_date
        )
        return url
