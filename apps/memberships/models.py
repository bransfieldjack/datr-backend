from django.db import models


class Membership(models.Model):
    profile = models.OneToOneField(
        'profiles.User', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type
