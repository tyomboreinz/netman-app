# Generated by Django 3.2.4 on 2021-10-13 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip_address',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
