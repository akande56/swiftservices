# Generated by Django 3.2.12 on 2023-08-14 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230814_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='preferences',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('cash', 'Cash'), ('offline_payment', 'Offline Payment'), ('partial_payment', 'Partial Payments')], max_length=400),
        ),
    ]
