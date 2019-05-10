import hmac
import base64
import hashlib
from datetime import datetime

TIME_STAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Credentials(object):
    """The authorization of transaction repository api."""

    def __init__(self, app_name, app_key, secret_key):
        """Initialize client class."""
        self.app_name = app_name
        self.app_key = app_key
        self.secret_key = secret_key

    def _get_valid_datetime(self):
        """Returns the current utc datetime in the correct timestamp"""
        now = datetime.utcnow()
        return now.strftime(TIME_STAMP_FORMAT)

    def build_token(self, token_datetime=None):
        """Build transaction repository api authorization token."""
        token_datetime = token_datetime or self._get_valid_datetime()

        raw_data = f"{self.app_name}{token_datetime}".upper()
        digestor = hmac.new(self.secret_key.encode(),
                            raw_data.encode(), hashlib.sha256)
        signature = base64.encodebytes(digestor.digest())
        signature = signature.decode().replace("\n", "")

        return f"{self.app_key};{signature};{token_datetime}"
