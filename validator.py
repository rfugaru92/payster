from datetime import datetime
import re


class Validator:
    def __call__(self, request):
        self._has_required(request)
        self._data = {}

        for key in VALIDATION_SCHEMA['properties'].keys():
            val = request.form.get(key)
            if val:
                if 'type' in VALIDATION_SCHEMA['properties'][key]:
                    assert(isinstance(val, VALIDATION_SCHEMA['properties'][key]['type']))

                if 'validation_method' in VALIDATION_SCHEMA['properties'][key]:
                    method = getattr(self, VALIDATION_SCHEMA['properties'][key]['validation_method'])
                    method(val)

                self._data[key] = val

        return self._data

    @staticmethod
    def isValidCard(value):
        """
        Guidelines from:
            * https://www.labnol.org/home/understand-credit-card-numbers/18527/
            * https://codereview.stackexchange.com/questions/169530/validating-credit-card-numbers
        :param value:
        :return:
        """
        pattern = '^([3456][0-9]{3})-?([0-9]{4})-?([0-9]{4})-?([0-9]{4})$'
        assert(re.match(pattern, value), "Card number is invalid.")

    @staticmethod
    def isValidDate(value):
        assert(datetime.strptime(value, '%Y-%m-%d'))

    @staticmethod
    def isValidSecurityCode(value):
        pattern = '^[0-9]{3}'
        assert(re.match(pattern, value))

    @staticmethod
    def isValidAmount(value):
        assert(value.isdecimal())
        assert(int(value) > 0)
        print(value.isdecimal())

    @staticmethod
    def _has_required(request):
        for prop in VALIDATION_SCHEMA['required']:
            assert(request.form.get(prop))


VALIDATION_SCHEMA = {
    'properties': {
        'creditCardNumber': {
            'type': str,
            'validation_method': 'isValidCard',
        },
        'cardHolder': {
            'type': str
        },
        'expirationDate': {
            'validation_method': 'isValidDate'
        },
        'securityCode': {
            'type': str,
            'validation_method': 'isValidSecurityCode'
        },
        'amount': {
            'validation_method': 'isValidAmount'
        }
    },
    'required': ['creditCardNumber', 'cardHolder', 'expirationDate', 'amount']
}
