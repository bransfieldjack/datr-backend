import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, status, views
from rest_framework.response import Response

from ...models import Membership
from .serializers import SubscriptionSerializer


class SubscriptionView(views.APIView):

    authentication_classes = [authentication.TokenAuthentication]

    @swagger_auto_schema(
        operation_description="Create and return a stripe checkout session.",
        manual_parameters=[
            openapi.Parameter("plan", openapi.IN_QUERY,
                              description="Stripe PlanID", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response("OK", SubscriptionSerializer)},
        request_body=SubscriptionSerializer
    )
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the validated data
        plan = serializer.validated_data.get('plan')
        _success_url = serializer.validated_data.get('success_url')
        _cancel_url = serializer.validated_data.get('cancel_url')

        # Create the checkout session on Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.create(
                success_url=_success_url,
                cancel_url=_cancel_url,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': plan,
                        'quantity': 1,
                    }
                ],
                mode='subscription',
            )
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already has a membership with the given plan
        try:
            membership = Membership.objects.get(profile=request.user, stripe_plan_id=plan)
            # If a membership with the given plan already exists, return a response indicating so
            return Response({'message': 'Membership already exists'}, status=status.HTTP_409_CONFLICT)
        except Membership.DoesNotExist:
            # If a membership with the given plan does not exist, create a new membership
            membership = Membership.objects.create(
                profile=request.user,
                stripe_plan_id=plan,
                stripe_checkout_session_id=session.id,
            )

            print("session resturns: ", session)
            # Return a success response with the session ID
            return Response({'session_id': session.id, "url": session.url}, status=status.HTTP_201_CREATED)


class SubscriptionSuccessView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        print("session called: ", session)
        print(" ")
        if session.subscription:
            # Save the subscription details to your database
            Membership.objects.create(
                profile=request.user,
                stripe_plan_id=session.subscription.items.data[0].price.id,
                stripe_checkout_session_id=session.subscription.id,
            )
        return render(request, 'subscription-success.html')


class SubscriptionCancelView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'subscription-cancel.html')