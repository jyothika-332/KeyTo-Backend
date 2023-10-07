from django.conf import settings
from rest_framework.views import APIView
import stripe
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status


stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePayment(APIView):
    def post(self,request):
        try:
            # Domain = self.request.data['origin_site']
            # checkout_session = stripe.checkout.Session.create(
            #     line_items=[
            #         {
            #             'price': 100,
            #             'quantity': 1,
            #         },
            #     ],
            #     mode='payment',
            #     success_url=Domain + '?success=true',
            #     cancel_url=Domain + '?canceled=true',
            # )
            session = stripe.checkout.Session.create(
            line_items=[{
            'price_data': {
                'currency': 'INR',
                'product_data': {
                'name': self.request.data['name'],
                },
                'unit_amount': self.request.data['price'] * 100,
            },
            'quantity': 1 ,
            }],
            mode='payment',
            success_url=self.request.data['origin_site'] + '/success=true',
            cancel_url=self.request.data['origin_site']  + '/canceled=true',
            
            )

            return Response({ "message" : session },status= status.HTTP_200_OK)
        except Exception as e:


            return Response({ "message" : str(e)},status= status.HTTP_500_INTERNAL_SERVER_ERROR)



