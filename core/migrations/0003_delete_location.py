# Generated by Django 4.0.6 on 2022-07-11 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_contact'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
    ]