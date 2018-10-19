import unittest as test
from main import app


class Tests(test.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)
        self.dummy_data = {
            'creditCardNumber': '4256-0222-3232-3232',
            'cardHolder': 'Radu',
            'expirationDate': '2019-01-19',
            'securityCode': '234',
            'amount': '245'
        }

    # Let the tests begin!
    def test_main_page(self):
        response = self.app.get('/pay')
        self.assertEqual(response.status_code, 200)

    def test_invalid_card_number(self):
        invalid_cards = ["1343-2234-2342-889", "4333-2212-43451234", "54351232534245"]

        for card in invalid_cards:
            self.dummy_data['creditCardNumber'] = card

            response = self.app.post(
                '/pay',
                data=self.dummy_data,
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 400)

    def test_expired_card(self):
        invalid_date = "2016-10-10"
        self.dummy_data['expirationDate'] = invalid_date

        response = self.app.post(
            '/pay',
            data=self.dummy_data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_security_code_too_long(self):
        security_code = "3433"
        self.dummy_data['securityCode'] = security_code

        response = self.app.post(
            '/pay',
            data=self.dummy_data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_negative_amount(self):
        invalid_amount = -10
        self.dummy_data['amount'] = invalid_amount

        response = self.app.post(
            '/pay',
            data=self.dummy_data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_zero_amount(self):
        invalid_amount = 0
        self.dummy_data['amount'] = invalid_amount

        response = self.app.post(
            '/pay',
            data=self.dummy_data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    test.main()
