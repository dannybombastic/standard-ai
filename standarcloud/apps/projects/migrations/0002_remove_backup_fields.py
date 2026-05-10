from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="projectconfig",
            name="auto_backup",
        ),
        migrations.RemoveField(
            model_name="projectconfig",
            name="backup_schedule",
        ),
    ]
