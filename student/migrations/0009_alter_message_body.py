# Generated by Django 4.2 on 2023-04-13 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0008_alter_message_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message", name="body", field=models.TextField(null=True),
        ),
    ]
