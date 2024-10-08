# Generated by Django 5.0.3 on 2024-09-15 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VdiInstance",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "instance_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_state",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_public_ip",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_private_ip",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_key_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_security_group",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_subnet_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_vpc_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_ami_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("instance_launch_time", models.DateTimeField()),
                ("instance_termination_time", models.DateTimeField()),
                ("instance_user_data", models.TextField(blank=True, null=True)),
                ("instance_tags", models.TextField(blank=True, null=True)),
                (
                    "instance_monitoring",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "instance_ebs_optimized",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "instance_public_dns",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_private_dns",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_architecture",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_hypervisor",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_virtualization_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_root_device_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_root_device_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_block_device_mappings",
                    models.TextField(blank=True, null=True),
                ),
                (
                    "instance_iam_instance_profile",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_network_interfaces",
                    models.TextField(blank=True, null=True),
                ),
                (
                    "instance_state_transition_reason",
                    models.TextField(blank=True, null=True),
                ),
                ("instance_state_reason", models.TextField(blank=True, null=True)),
                ("instance_cpu_options", models.TextField(blank=True, null=True)),
                (
                    "instance_capacity_reservation_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_capacity_reservation_specification",
                    models.TextField(blank=True, null=True),
                ),
                ("instance_metadata_options", models.TextField(blank=True, null=True)),
                ("instance_enclave_options", models.TextField(blank=True, null=True)),
                (
                    "instance_elastic_gpu_associations",
                    models.TextField(blank=True, null=True),
                ),
                (
                    "instance_elastic_inference_accelerator_associations",
                    models.TextField(blank=True, null=True),
                ),
                (
                    "instance_outpost_arn",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "instance_auto_scaling_group_associations",
                    models.TextField(blank=True, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
