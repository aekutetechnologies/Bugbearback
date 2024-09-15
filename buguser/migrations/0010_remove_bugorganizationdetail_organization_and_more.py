# Generated by Django 5.0.3 on 2024-09-10 09:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buguser", "0009_rename_skill_description_bugbearskill_description_and_more"),
        ("jobs", "0005_alter_bugjob_company"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bugorganizationdetail",
            name="organization",
        ),
        migrations.RemoveField(
            model_name="bugorganizationdetail",
            name="org_address",
        ),
        migrations.RemoveField(
            model_name="bugorganizationdetail",
            name="org_city",
        ),
        migrations.RemoveField(
            model_name="bugorganizationdetail",
            name="org_country",
        ),
        migrations.RemoveField(
            model_name="bugorganizationdetail",
            name="org_description",
        ),
        migrations.RemoveField(
            model_name="bugorganizationdetail",
            name="org_phone",
        ),
        migrations.RemoveField(
            model_name="bugorganizationdetail",
            name="org_profile_pic",
        ),
        migrations.RemoveField(
            model_name="bugorganizationdetail",
            name="org_website",
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="current_company_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="current_designation",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="current_location",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="first_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="last_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="state",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="organization",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="bugorganizationdetail",
            name="zip_code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="mobile",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.DeleteModel(
            name="BugOrganization",
        ),
    ]
