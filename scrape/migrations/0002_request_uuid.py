# Generated by Django 2.2 on 2020-10-13 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='uuid',
            field=models.TextField(null=True),
        ),
    ]
