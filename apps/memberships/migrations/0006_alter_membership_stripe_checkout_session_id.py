# Generated by Django 4.1.7 on 2023-04-02 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0005_membership_stripe_checkout_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='stripe_checkout_session_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]