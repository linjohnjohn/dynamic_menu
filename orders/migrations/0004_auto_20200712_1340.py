# Generated by Django 3.0.8 on 2020-07-12 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_session'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='transaction_id',
            new_name='stripe_checkout_id',
        ),
    ]
