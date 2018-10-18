from datetime import datetime
import re


class Validator:
    def __call__(self, request):
        self._has_required(request)
        self._data = {}

        for key in VALIDATION_SCHEMA['properties'].keys():
            val = request.form.get(key)
            if val:
                print(key)
                if 'type' in VALIDATION_SCHEMA['properties'][key]:
                    assert(isinstance(val, VALIDATION_SCHEMA['properties'][key]['type']))

                if 'validation_method' in VALIDATION_SCHEMA['properties'][key]:
                    method = getattr(self, VALIDATION_SCHEMA['properties'][key]['validation_method'])
                    method(val)

        return self._data

    def isValidCard(self, value):
        """
        Guidelines from:
            * https://www.labnol.org/home/understand-credit-card-numbers/18527/
            * https://codereview.stackexchange.com/questions/169530/validating-credit-card-numbers
        :param value:
        :return:
        """
        pattern = '^([3456][0-9]{3})-?([0-9]{4})-?([0-9]{4})-?([0-9]{4})$'
        assert(re.match(pattern, value), "Card number is invalid.")

    def isValidDate(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except:
            raise Exception("Input string does not have valid date format.")

    def isValidSecurityCode(self, value):
        pattern = '^[0-9]{3}'
        assert(re.match(pattern, value))

    def isValidAmount(self, value):
        assert(value.isdecimal(), "Amount must be decimal.")
        assert(value > 0, "Amount must have a positive value.")

    def _has_required(self, request):
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
            'validate_method': 'isValidSecurityCode'
        },
        'amount': {
            'validate_method': 'isValidAmount'
        }
    },
    'required': ['creditCardNumber', 'cardHolder', 'expirationDate', 'amount']
}
