# Generated by Django 2.2.6 on 2021-04-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_amount_diposite_slip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amount',
            name='diposite_slip',
            field=models.ImageField(blank=True, default='diposite.jpg', null=True, upload_to='images/amounts/'),
        ),
    ]