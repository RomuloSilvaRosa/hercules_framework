
from boto3 import Session
from boto3 import session as boto3session
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

from hercules_framework.settings import AWS_REGION
from hercules_framework.utils import unique


class RefreshableSession:
    session: Session
    base_session = boto3session.Session()

    def __init__(self, arn: str, session_name: str=unique(),
                 aws_region: str = AWS_REGION, duration=3600):
        self._arn = arn
        self._session_name = session_name
        self._aws_region = aws_region
        self._duration = duration
        self._sts_client = self.base_session.client("sts",
                                               region_name=self._aws_region)
        session = get_session()
        session._credentials = RefreshableCredentials.create_from_metadata(
            metadata=self._refresh(),
            refresh_using=self._refresh,
            method="sts-assume-role",
        )
        session.set_config_variable("region", self._aws_region)
        self.session = Session(botocore_session=session)

    def _refresh(self):
        " Refresh tokens by calling assume_role again "
        params = {
            "RoleArn": self._arn,
            "RoleSessionName": self._session_name,
            "DurationSeconds": self._duration,
        }

        response = self._sts_client.assume_role(**params).get("Credentials")
        credentials = {
            "access_key": response.get("AccessKeyId"),
            "secret_key": response.get("SecretAccessKey"),
            "token": response.get("SessionToken"),
            "expiry_time": response.get("Expiration").isoformat(),
        }
        return credentials
