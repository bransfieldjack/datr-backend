# Generated by Django 4.1.7 on 2023-04-02 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0004_membership_trial_ends_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='stripe_checkout_session_id',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
