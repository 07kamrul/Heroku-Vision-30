# Generated by Django 2.2.6 on 2021-04-25 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_aboutus_aboutus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vision',
            name='point',
        ),
    ]
