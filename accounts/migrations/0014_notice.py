# Generated by Django 2.2.6 on 2021-04-27 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20210426_0539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice', models.CharField(blank=True, max_length=100, null=True)),
                ('descriptions', models.CharField(blank=True, max_length=1000, null=True)),
                ('publish_date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
