# Generated by Django 2.2.6 on 2021-04-24 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210424_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]