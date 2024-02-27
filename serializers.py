from rest_framework import serializers

class CreateDockerImageSerializer(serializers.Serializer):
    data = serializers.CharField()