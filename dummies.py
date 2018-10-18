class ICheapPaymentGateway:
    available = True

    def connect(self):
        if self.available:
            return True
        else:
            raise Exception("Failed to connect to gateway")

    def process_payment(self, data):
        if self.available:
            return True
        else:
            raise Exception("Failed to connect to gateway")


class IExpensivePaymentGateway:
    available = True

    def connect(self):
        if self.available:
            return True
        else:
            raise Exception("Failed to connect to gateway")

    def process_payment(self, data):
        if self.available:
            return True
        else:
            raise Exception("Failed to connect to gateway")


class IPremiumPaymentGateway:
    available = False

    def connect(self):
        if self.available:
            return True
        else:
            raise Exception("Failed to connect to gateway")

    def process_payment(self, data):
        if self.available:
            return True
        else:
            raise Exception("Failed to connect to gateway")
