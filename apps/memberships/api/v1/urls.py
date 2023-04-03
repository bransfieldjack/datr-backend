# urls.py
from django.urls import path
from .views import SubscriptionView, SubscriptionSuccessView, SubscriptionCancelView

urlpatterns = [
    path('subscriptions/', SubscriptionView.as_view()),
    path('subscription-success/', SubscriptionSuccessView.as_view(), name='subscription-success'),
    path('subscription-cancel/', SubscriptionCancelView.as_view(), name='subscription-cancel'),
]
