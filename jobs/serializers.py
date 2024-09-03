from rest_framework import serializers
from .models import BugJob
from buguser.models import BugOrganization as Company

class JobSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = BugJob
        fields = '__all__'


class JobTitleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
