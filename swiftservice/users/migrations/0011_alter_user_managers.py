# Generated by Django 3.2.12 on 2023-09-07 19:13

from django.db import migrations
import swiftservice.users.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', swiftservice.users.managers.UserManager()),
            ],
        ),
    ]
