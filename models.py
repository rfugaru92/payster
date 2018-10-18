import sys

from validator import Validator
import re


class Payment(object):
    def __init__(self, data):
        self.data = data

    def execute_payment(self):
        gateway_name = self.get_payment_gateway()
        PaymentGateway = getattr(sys.modules[__name__], gateway_name)

        client = PaymentGateway()
        # Connecting to dummy gateway client
        try:
            client.connect()
            client.process_payment(self.data)
        except:
            if PAYMENT_GATEWAYS[gateway_name]['retries']:
                result = self.retry_payment(client, PAYMENT_GATEWAYS[gateway_name]['retries'])
                if result:
                    return True

    def retry_payment(self, client, left):
        try:
            client.connect()
            client.process_payment(self.data)
            return True
        except:
            if left:
                self.retry_payment(client, left-1)
            return False

    def get_payment_gateway(self):
        if self.data['amount'] <=20:
            return 'ICheapPaymentGateway'
        elif 20 < self.data['amount'] <= 500:
            return 'IExpensivePaymentGateway'
        else:
            return 'IPremiumPaymentGateway'


PAYMENT_GATEWAYS = {
    'ICheapPaymentGateway': {
        'retries': 0
    },
    'IExpensivePaymentGateway': {
        'retries': 0,
        'alt': 'ICheapPaymentGateway',
        'retries_alt': 1
    },
    'IPremiumPaymentGateway': {
        'retries': 3
    }
}