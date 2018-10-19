import sys


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
                    return

            if 'alt' in PAYMENT_GATEWAYS[gateway_name].keys():
                AltGateway = getattr(sys.modules[__name__], PAYMENT_GATEWAYS[gateway_name]['alt'])
                alt_client = AltGateway()
                if PAYMENT_GATEWAYS[gateway_name]['retries_alt']:
                    result = self.retry_payment(alt_client, PAYMENT_GATEWAYS[gateway_name]['retries_alt'])
                    if result:
                        return

            raise Exception('Failed to process payment.')

    def retry_payment(self, client, tries_left):
        try:
            client.connect()
            client.process_payment(self.data)
            return True
        except:
            if tries_left:
                self.retry_payment(client, tries_left - 1)
            return False

    def get_payment_gateway(self):
        if int(self.data['amount']) <= 20:
            return 'ICheapPaymentGateway'
        elif 20 < int(self.data['amount']) <= 500:
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