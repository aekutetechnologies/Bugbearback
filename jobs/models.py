from django.db import models
from buguser.models import BugOrganization

# Create your models here.

class BugJobCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  # e.g., Engineering

    def __str__(self):
        return self.name


class BugJob(models.Model):
    JOB_TYPE_CHOICES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Contract", "Contract"),
        ("Internship", "Internship"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # e.g., Senior UX Designer
    company = models.ForeignKey(
        BugOrganization, on_delete=models.CASCADE, related_name="jobs"
    )  # Company relation
    job_description = models.TextField()  # BugJob description field
    category = models.ForeignKey(
        BugJobCategory, on_delete=models.CASCADE, related_name="jobs", null=True
    )  # Job category relation
    responsibilities = models.TextField()  # Responsibilities section
    job_posted = models.DateField()  # BugJob posted date
    job_expiry = models.DateField()  # BugJob expiry date
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)  # Minimum salary
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)  # Maximum salary
    location = models.CharField(max_length=255)  # e.g., New York, USA
    job_type = models.CharField(
        max_length=50, choices=JOB_TYPE_CHOICES, default="Full Time"
    )
    experience = models.FloatField(default=0.0)
    education = models.CharField(
        max_length=255, default="Graduation"
    )  # e.g., Graduation
    featured = models.BooleanField(default=False)  # Is this job featured?

    def __str__(self):
        return self.title
