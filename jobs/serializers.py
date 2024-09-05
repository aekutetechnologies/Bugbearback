from rest_framework import serializers
from .models import BugJob
from buguser.models import BugOrganization as Company
from buguser.serializers import BugOrganizationSerializer


class JobSerializer(serializers.ModelSerializer):
    organisation = BugOrganizationSerializer(source='company', read_only=True)

    class Meta:
        model = BugJob
        fields = ["id", "title", "job_description", "responsibilities", "job_posted", "job_expiry",
                  "salary_min", "salary_max", "location", "job_type", "experience", "education", "featured",
                  "organisation"]


class JobTitleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
