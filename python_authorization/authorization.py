"""This module is used to handle authorization at the API"""
import json
from datetime import datetime, timedelta
from .credentials import Credentials

TIME_STAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Authorization(object):
    def __init__(
            self, token, token_expiration_time=30,
            valid_credentials_dict=None):
        """The Authorization constructor receives a raw token as a parameter"""
        self.token = token
        self.expiration_in_seconds = token_expiration_time
        self.valid_credentials = valid_credentials_dict

    def _get_app_info(self, app_key):
        """This method read from the environment variable and serialize as a
        JSON that follows this format: {'app_key':['app_name','secret_key']}"""
        return self.valid_credentials.get(app_key)

    def validate_token_format(self):
        """This method validate that the token format is a valid one by
        validating all the : characters that it contains"""
        token_slices = self.token.split(';')
        if len(token_slices) == 3:
            # We need to check if any of the token slices is empty
            for token_slice in token_slices:
                if len(token_slice) == 0:
                    return False
            return True
        return False

    def _validate_token_date(self, token_datetime):
        """This method validate that the token date provided as token_datetime
        is in the valid range"""
        token_date = datetime.strptime(token_datetime, TIME_STAMP_FORMAT)
        now = datetime.utcnow()
        past_expiration_date = now - timedelta(
            seconds=self.expiration_in_seconds)
        future_expiration_date = now + timedelta(
            seconds=self.expiration_in_seconds)

        if token_date >= past_expiration_date \
                and token_date <= future_expiration_date:
            return True

        return False

    def _parse_app_info(self, app_info):
        """This method parse the app information raw data"""
        # The app name is the first part of the app information
        app_name = app_info[0]
        # The secret key is the second part of the app information
        secret_key = app_info[1]

        return (app_name, secret_key)

    def _parse_token(self):
        """This method deals with the raw token and returns its individual
        parts as a tuple"""
        # The token is composed of 3 parts separated by a ;
        # we split the token by ; and then treat the slices
        token_slices = self.token.split(';')

        # The app key is the first part of the token
        app_key = token_slices[0]

        # The datetime is the third part of the token
        token_datetime = token_slices[2]

        # The app information is contained inside the app_key
        app_info = self._get_app_info(app_key)

        return (app_key, token_datetime, app_info)

    def validate_token(self):
        """This methods validates the token as a whole."""
        # Get token primary parts
        app_key, token_datetime, app_info = self._parse_token()

        # If we were unable to find the app information, the token is invalid
        if not app_info:
            return False

        # Get token secondary parts inside the app information
        app_name, secret_key = self._parse_app_info(app_info)

        # Validate if the token date is still valid
        is_valid = self._validate_token_date(token_datetime)
        if not is_valid:
            return False

        signer = Credentials(
            app_name, app_key, secret_key)

        # Validate if the token is valid as a whole
        if signer.build_token(token_datetime) == self.token:
            return True
        return False
