# Generated by Django 2.2.6 on 2021-04-18 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210318_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amount',
            name='diposite_slip',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]