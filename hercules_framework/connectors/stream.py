
import json

from boto3_type_annotations.firehose import Client
from botocore.session import get_session

from hercules_framework.settings import (ENABLE_STREAM, FIREHOSE_ROLE,
                                         KINESIS_FIREHOSE_STREAM_DATA_NAME,OUT_FOLDER)
from hercules_framework.utils import datenow
from hercules_framework.utils.mkdir_p import mkdir_p

class FakeStream:
    """Fake Stream to help local tests
    """

    def put_record(self, *args, **kwargs):
        mkdir_p(OUT_FOLDER)
        with open(OUT_FOLDER + KINESIS_FIREHOSE_STREAM_DATA_NAME + '.dms', 'a+') as file:
            file.write(kwargs.get('Record', {}).get('Data'))


class Stream:
    session = None

    def __init__(self, logger=None):
        if ENABLE_STREAM:
            self.session = get_session()
            self.stream: Client = self.session.client('firehose')

        else:
            self.stream = FakeStream()
        self.logger = logger

    def set_logger(self, logger):
        self.logger = logger

    def send_stream_dict(self, body: dict):
        try:
            self.logger.info("Sending stream dict")
            self.stream.put_record(
                DeliveryStreamName=KINESIS_FIREHOSE_STREAM_DATA_NAME,
                Record={
                    'Data': json.dumps((body)) + "\n"
                }
            )
        except Exception:
            self.logger.info('Error trying to send stream dict')

    def send_data(self, data: dict, record_type: str):
        """Send data to Kinesis with current date and record type 

        Arguments:
            data {dict} -- The sent data 
            record_type {str} -- The record type
        """
        new_data = Stream.set_record_type(record_type, data)
        new_data = Stream.set_date_now(new_data)
        self.send_stream_dict(new_data)

    @staticmethod
    def set_record_type(record_type: str, data: dict) -> dict:
        data['RecordType'] = record_type
        return data

    @staticmethod
    def set_date_now(data):
        data['created_at'] = datenow()
        return data
