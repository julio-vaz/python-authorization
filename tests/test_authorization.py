from datetime import datetime, timedelta
from python_authorization import (
    Authorization,
    Credentials
)
from unittest.mock import patch
import unittest

TIME_STAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
MOCK_DATETIME = "2019-01-29T23:32:30Z"
MOCK_APP_KEY = "Festa"
MOCK_SECRET = "12312312312312312312312312312312312"
MOCK_APP_NAME = "Brasil"
MOCK_APP_INFO = [MOCK_APP_NAME, MOCK_SECRET]
MOCK_EXPIRATION = {
    'TOKEN_EXPIRATION_IN_SECONDS': '30'
}


class TestAuthorization(unittest.TestCase):
    def _generate_token(self,
                        app_name=MOCK_APP_NAME,
                        app_key=MOCK_APP_KEY,
                        secret=MOCK_SECRET):
        credentials = Credentials(
            app_name,
            app_key,
            secret
        )
        return credentials.build_token()

    def setUp(self):
        self.valid_base = "Festa;4QnileeUB0iBt00AVqgctVc1vUfCpIwS/TJjmWnH6SE=;"
        self.invalid_base = "Bar;6JyhneeUB0iBt00AVqgctVc1vUfCpIwS/TJjmWnH6TG=;"
        self.valid_mock_token = f"{self.valid_base}{MOCK_DATETIME}"
        self.invalid_mock_token = f"{self.invalid_base}{MOCK_DATETIME}"

    @patch.object(Credentials,
                  "_get_valid_datetime",
                  return_value=MOCK_DATETIME)
    def test_valid_token_without_custom_date(self, mock_get_valid_datetime):
        token = self._generate_token()
        self.assertEqual(token, self.valid_mock_token)

    @patch.object(Credentials,
                  "_get_valid_datetime",
                  return_value=MOCK_DATETIME)
    def test_invalid_app_name_without_custom_date(
            self, mock_get_valid_datetime):
        token = self._generate_token(app_name="InvalidAppName")
        self.assertNotEqual(token, self.valid_mock_token)

    @patch.object(Credentials,
                  "_get_valid_datetime",
                  return_value=MOCK_DATETIME)
    def test_invalid_app_key_without_custom_date(self, mock_get_valid):
        token = self._generate_token(app_key="InvalidAppKey")
        self.assertNotEqual(token, self.valid_mock_token)

    @patch.object(Credentials,
                  "_get_valid_datetime",
                  return_value=MOCK_DATETIME)
    def test_invalid_secret_without_custom_date(self, mock_get_valid):
        token = self._generate_token(secret="InvalidSecret")
        self.assertNotEqual(token, self.valid_mock_token)

    def test_valid_token_with_custom_date(self):
        credentials = Credentials(
            MOCK_APP_NAME,
            MOCK_APP_KEY,
            MOCK_SECRET
        )
        token = credentials.build_token(MOCK_DATETIME)

        self.assertEqual(token, self.valid_mock_token)

    @patch.dict('os.environ', MOCK_EXPIRATION)
    @patch.object(Authorization,
                  "_get_app_info",
                  return_value=MOCK_APP_INFO)
    @patch.object(Authorization,
                  '_validate_token_date',
                  return_value=True)
    def test_valid_token_validation(self, mock_get_app_info, mock_date):
        validater = Authorization(self.valid_mock_token)
        is_valid = validater.validate_token()
        self.assertTrue(is_valid)

    @patch.dict('os.environ', MOCK_EXPIRATION)
    @patch.object(Authorization,
                  "_get_app_info",
                  return_value=MOCK_APP_INFO)
    @patch.object(Authorization,
                  '_validate_token_date',
                  return_value=True)
    def test_invalid_token_validation(self, mock_get_app_info, mock):
        validater = Authorization(self.invalid_mock_token)
        is_valid = validater.validate_token()
        self.assertFalse(is_valid)

    @patch.dict('os.environ', MOCK_EXPIRATION)
    def test_invalid_token_format(self):
        validater = Authorization(self.invalid_base)
        is_valid = validater.validate_token_format()
        self.assertFalse(is_valid)

    @patch.dict('os.environ', MOCK_EXPIRATION)
    def test_valid_token_format(self):
        validater = Authorization(self.valid_mock_token)
        is_valid = validater.validate_token_format()
        self.assertTrue(is_valid)

    @patch.dict('os.environ', MOCK_EXPIRATION)
    @patch.object(Authorization,
                  "_get_app_info",
                  return_value=MOCK_APP_INFO)
    def test_valid_now_date_token_validation(self, mock_get_app_info):
        now = datetime.utcnow().strftime(TIME_STAMP_FORMAT)
        validater = Authorization(None)
        is_valid = validater._validate_token_date(now)
        self.assertTrue(is_valid)

    @patch.dict('os.environ', MOCK_EXPIRATION)
    @patch.object(Authorization,
                  "_get_app_info",
                  return_value=MOCK_APP_INFO)
    def test_valid_before_past_expire_date_token_validation(
            self, mock_get_app_info):
        valid_date = datetime.utcnow() - timedelta(seconds=27)
        now = valid_date.strftime(TIME_STAMP_FORMAT)
        validater = Authorization(None)
        is_valid = validater._validate_token_date(now)
        self.assertTrue(is_valid)

    @patch.dict('os.environ', MOCK_EXPIRATION)
    @patch.object(Authorization,
                  "_get_app_info",
                  return_value=MOCK_APP_INFO)
    def test_valid_before_future_expire_date_token_validation(
            self, mock_get_app_info):
        valid_date = datetime.utcnow() + timedelta(seconds=27)
        now = valid_date.strftime(TIME_STAMP_FORMAT)
        validater = Authorization(None)
        is_valid = validater._validate_token_date(now)
        self.assertTrue(is_valid)

    @patch.object(Authorization,
                  "_get_app_info",
                  return_value=MOCK_APP_INFO)
    def test_invalid_past_date_token_validation(
            self, mock_get_app_info):
        invalid_date = datetime.utcnow() - timedelta(seconds=30)
        now = invalid_date.strftime(TIME_STAMP_FORMAT)
        validater = Authorization(None, 30)
        is_valid = validater._validate_token_date(now)
        self.assertFalse(is_valid)

    @patch.object(Authorization,
                  "_get_app_info",
                  return_value=MOCK_APP_INFO)
    def test_invalid_future_date_token_validation(
            self, mock_get_app_info):
        invalid_date = datetime.utcnow() + timedelta(seconds=31)
        now = invalid_date.strftime(TIME_STAMP_FORMAT)
        validater = Authorization(None, 30)
        is_valid = validater._validate_token_date(now)
        self.assertFalse(is_valid)
