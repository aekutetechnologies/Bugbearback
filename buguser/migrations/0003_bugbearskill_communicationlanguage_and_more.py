# Generated by Django 5.0.3 on 2024-05-09 12:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "buguser",
            "0002_alter_buguserdetail_address_alter_buguserdetail_city_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="BugBearSkill",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("skill_name", models.CharField(max_length=50)),
                ("skill_description", models.TextField()),
                ("skill_logo", models.ImageField(upload_to="skill_logos/")),
            ],
        ),
        migrations.CreateModel(
            name="CommunicationLanguage",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("language_name", models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name="buguserdetail",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female")],
                default="Male",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="BugUserSkill",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "skill_level",
                    models.CharField(
                        choices=[
                            ("Beginner", "Beginner"),
                            ("Intermediate", "Intermediate"),
                            ("Expert", "Expert"),
                        ],
                        default="Beginner",
                        max_length=20,
                    ),
                ),
                (
                    "skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="buguser.bugbearskill",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UsersCommunicationLanguage",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "language_level",
                    models.CharField(
                        choices=[
                            ("Beginner", "Beginner"),
                            ("Intermediate", "Intermediate"),
                            ("Expert", "Expert"),
                        ],
                        default="Beginner",
                        max_length=20,
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="buguser.communicationlanguage",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
