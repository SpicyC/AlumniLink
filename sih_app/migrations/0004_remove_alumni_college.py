# Generated by Django 2.2.3 on 2020-01-10 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sih_app', '0003_alumni_college'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumni',
            name='college',
        ),
    ]
