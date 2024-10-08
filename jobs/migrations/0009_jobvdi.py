# Generated by Django 5.0.3 on 2024-09-16 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0008_jobsapplied_is_approved"),
        ("vdi", "0002_alter_vdiinstance_instance_launch_time_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobVdi",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jobs.bugjob"
                    ),
                ),
                (
                    "vdi",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vdi.vdiinstance",
                    ),
                ),
            ],
        ),
    ]
