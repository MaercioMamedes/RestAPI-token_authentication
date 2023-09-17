from rest_framework import serializers


class RegisterUpdateSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=11, required=False)
    username = serializers.CharField(max_length=50, required=False)
    email = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=50, required=False)
    password_confirm = serializers.CharField(max_length=50, required=False)

    def create(self, validated_data):
        pass
