from rest_framework import serializers

from .models import Review
from users.serializers import UserShortInfoSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserShortInfoSerializer()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
