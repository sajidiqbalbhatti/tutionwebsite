from django.shortcuts import render

# Create your views here.
# views.py

from django.views import View
from django.shortcuts import redirect
from django.conf import settings
from payments.payfast import PayFastAPI
class PayFastCheckoutView(View):
    def get(self, request, *args, **kwargs):
        amount = 1000
        item_name = "Codexa Python Course"
        user_email = "testuser@example.com"

        payfast = PayFastAPI(
            merchant_id=settings.PAYFAST_MERCHANT_ID,  # now using test ID
            merchant_key=settings.PAYFAST_MERCHANT_KEY,  # now using test key
            passphrase=settings.PAYFAST_PASSPHRASE,
            return_url='http://localhost:8000/payment/success/',
            cancel_url='http://localhost:8000/payment/cancel/',
            notify_url='http://localhost:8000/payment/notify/',
            sandbox=True  # 🔁 test mode ON
        )

        payment_url = payfast.get_payment_url(amount, item_name, user_email)
        print("✅ Payment URL:", payment_url)  # terminal mein check karo

        return redirect(payment_url)
# views.py

from django.views.generic import TemplateView

class CheckoutPageView(TemplateView):
    template_name = "payment/checkout.html"
