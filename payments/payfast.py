# payments/payfast.py

import hashlib
from urllib.parse import urlencode

class PayFastAPI:
    def __init__(self, merchant_id, merchant_key, passphrase, return_url, cancel_url, notify_url, sandbox=True):
        self.merchant_id = merchant_id
        self.merchant_key = merchant_key
        self.passphrase = passphrase
        self.return_url = return_url
        self.cancel_url = cancel_url
        self.notify_url = notify_url
        self.sandbox = sandbox
        self.gateway_url = "https://sandbox.payfast.pk/eng/process" if sandbox else "https://www.payfast.pk/eng/process"

    def get_payment_url(self, amount, item_name, user_email):
        data = {
            'merchant_id': self.merchant_id,
            'merchant_key': self.merchant_key,
            'return_url': self.return_url,
            'cancel_url': self.cancel_url,
            'notify_url': self.notify_url,
            'amount': "%.2f" % float(amount),
            'item_name': item_name,
            'email_address': user_email,
        }

        # Signature generate karo
        data_string = urlencode(data)
        if self.passphrase:
            data_string += f"&passphrase={self.passphrase}"
        signature = hashlib.md5(data_string.encode('utf-8')).hexdigest()

        data['signature'] = signature
        return f"{self.gateway_url}?{urlencode(data)}"
