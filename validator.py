from datetime import datetime
import re


class Validator:
    def __call__(self, *args, **kwargs):
        request = args[0]
        self._has_required(request)
        self._data = {}

        for key in VALIDATION_SCHEMA['properties'].keys():
            val = request.form.get(key)
            if val:
                if 'type' in VALIDATION_SCHEMA['properties'][key]:
                    if not isinstance(val, VALIDATION_SCHEMA['properties'][key]['type']):
                        raise Exception('Wrong field type for %s', key)

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
        if not re.match(pattern, value):
            raise Exception('Credit card number is invalid.')

    @staticmethod
    def isValidDate(value):
        try:
            date = datetime.strptime(value, '%Y-%m-%d')
        except:
            raise Exception("Date format is invalid.")

        assert(date > datetime.now())

    @staticmethod
    def isValidSecurityCode(value):
        pattern = '^([0-9]{3})$'
        assert(re.match(pattern, value))

    @staticmethod
    def isValidAmount(value):
        assert(value.isdecimal())
        assert(int(value) > 0)

    @staticmethod
    def _has_required(request):
        for prop in VALIDATION_SCHEMA['required']:
            if not request.form.get(prop):
                raise Exception("Field %s is required.", prop)


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
