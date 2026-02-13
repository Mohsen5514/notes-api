from rest_framework import serializers
from .models import *



class TaskSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField()
    class Meta:
        model=Task
        fields='__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title too short")
        return value
