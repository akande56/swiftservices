# Generated by Django 3.2.12 on 2023-09-07 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serviceprovider',
            old_name='skills',
            new_name='service',
        ),
    ]