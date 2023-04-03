from django.db import models


class Membership(models.Model):
    profile = models.OneToOneField(
        'profiles.User', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    stripe_plan_id = models.CharField(max_length=40)
    stripe_checkout_session_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.stripe_plan_id
