from validator import Validator
import re


class Payment(object):
    def __init__(self, creditCardNumber, cardHolder, expirationDate, amount, securityCode=None):
        self.creditCardNumber = creditCardNumber
        self.cardHolder = cardHolder
        self.expirationDate = expirationDate
        self.securityCode = securityCode

        self.amount = amount

    @property
    def creditCardNumber(self):
        return self._creditCardNumber

    @creditCardNumber.setter
    def creditCardNumber(self, value):
        self._creditCardNumber = Validator(value)

    @property
    def cardHolder(self):
        return self._cardHolder

    @cardHolder.setter
    def cardHolder(self, value):
        self._cardHolder = Validator(value)

    @property
    def expirationDate(self):
        return self._expirationDate

    @expirationDate.setter
    def expirationDate(self, value):
        self._expirationDate = Validator(value)

    @property
    def securityCode(self):
        return self._securityCode

    @securityCode.setter
    def securityCode(self, value):
        self._securityCode = Validator(value)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = Validator(value)
