from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=11)
    username = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    password_confirm = serializers.CharField(max_length=100)

    def create(self, validated_data):
        pass
